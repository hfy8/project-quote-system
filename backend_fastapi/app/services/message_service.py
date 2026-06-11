from app import db
from app.models import Message


class MessageService:
    """消息服务 - 封装消息发送逻辑"""
    
    # 消息类型常量
    TYPE_MODULE_MEMBER_ADDED = 'module_member_added'
    TYPE_CHANGE_REQUEST_SUBMITTED = 'change_request_submitted'
    TYPE_CHANGE_REQUEST_APPROVED = 'change_request_approved'
    TYPE_CHANGE_REQUEST_REJECTED = 'change_request_rejected'
    TYPE_VERSION_UPDATED = 'version_updated'
    TYPE_PARTICIPANT_ADDED = 'participant_added'
    
    @staticmethod
    def send_message(recipient_id, title, content, msg_type, related_id=None, related_type=None, sender_id=None):
        """发送消息"""
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            title=title,
            content=content,
            type=msg_type,
            related_id=related_id,
            related_type=related_type
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def send_to_users(user_ids, title, content, msg_type, related_id=None, related_type=None):
        """向多个用户发送消息"""
        messages = []
        for user_id in user_ids:
            message = Message(
                sender_id=None,
                recipient_id=user_id,
                title=title,
                content=content,
                type=msg_type,
                related_id=related_id,
                related_type=related_type
            )
            messages.append(message)
        db.session.bulk_save_objects(messages)
        db.session.commit()
        return len(messages)
    
    @classmethod
    def notify_module_member_added(cls, user_id, quotation_name, module_name, quotation_id):
        """通知成员被添加到模块"""
        return cls.send_message(
            recipient_id=user_id,
            title=f'你已被添加到项目模块',
            content=f'你已被添加到"{quotation_name}"项目的"{module_name}"模块',
            msg_type=cls.TYPE_MODULE_MEMBER_ADDED,
            related_id=quotation_id,
            related_type='quotation'
        )
    
    @classmethod
    def notify_change_request_submitted(cls, business_owner_id, requester_name, quotation_name, module_name, change_type, change_request_id):
        """通知业务员有新的变更申请"""
        change_type_map = {
            'material_add': '添加物料',
            'material_update': '修改物料',
            'material_delete': '删除物料'
        }
        type_label = change_type_map.get(change_type, change_type)
        
        return cls.send_message(
            recipient_id=business_owner_id,
            title=f'新的变更申请',
            content=f'{requester_name}提交了"{quotation_name}"项目中"{module_name}"的{type_label}申请，请尽快审核',
            msg_type=cls.TYPE_CHANGE_REQUEST_SUBMITTED,
            related_id=change_request_id,
            related_type='change_request'
        )
    
    @classmethod
    def notify_change_request_approved(cls, requester_id, quotation_name, module_name, change_type, change_request_id):
        """通知申请人变更已批准"""
        change_type_map = {
            'material_add': '添加物料',
            'material_update': '修改物料',
            'material_delete': '删除物料'
        }
        type_label = change_type_map.get(change_type, change_type)
        
        return cls.send_message(
            recipient_id=requester_id,
            title=f'变更申请已批准',
            content=f'你在"{quotation_name}"项目的"{module_name}"中提交的{type_label}申请已批准',
            msg_type=cls.TYPE_CHANGE_REQUEST_APPROVED,
            related_id=change_request_id,
            related_type='change_request'
        )
    
    @classmethod
    def notify_change_request_rejected(cls, requester_id, quotation_name, module_name, change_type, change_request_id, reason=None):
        """通知申请人变更被拒绝"""
        change_type_map = {
            'material_add': '添加物料',
            'material_update': '修改物料',
            'material_delete': '删除物料'
        }
        type_label = change_type_map.get(change_type, change_type)
        
        content = f'你在"{quotation_name}"项目的"{module_name}"中提交的{type_label}申请被拒绝'
        if reason:
            content += f'，原因：{reason}'
        
        return cls.send_message(
            recipient_id=requester_id,
            title=f'变更申请被拒绝',
            content=content,
            msg_type=cls.TYPE_CHANGE_REQUEST_REJECTED,
            related_id=change_request_id,
            related_type='change_request'
        )
    
    @classmethod
    def notify_version_updated(cls, user_ids, quotation_name, version_no, quotation_id):
        """通知报价单版本更新"""
        return cls.send_to_users(
            user_ids=user_ids,
            title=f'报价单版本更新',
            content=f'"{quotation_name}"已更新到v{version_no}版本',
            msg_type=cls.TYPE_VERSION_UPDATED,
            related_id=quotation_id,
            related_type='quotation'
        )

    @classmethod
    def notify_participant_added(cls, user_id, quotation_name, participant_type, added_by_name, quotation_id):
        """通知用户被添加为报价单参与人"""
        type_map = {
            'project': '项目',
            'agency': '机构',
            'electrical': '电气',
            'engineer': '工程师'
        }
        type_label = type_map.get(participant_type, participant_type)
        return cls.send_message(
            recipient_id=user_id,
            title='你已被添加为报价单参与人',
            content=f'你已被添加为"{quotation_name}"的{type_label}参与人，由{added_by_name}添加',
            msg_type=cls.TYPE_PARTICIPANT_ADDED,
            related_id=quotation_id,
            related_type='quotation'
        )