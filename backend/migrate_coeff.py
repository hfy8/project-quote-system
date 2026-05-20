from app import create_app, db
app = create_app()
with app.app_context():
    try:
        db.session.execute(db.text("ALTER TABLE quotations ADD COLUMN coefficients JSON"))
        db.session.commit()
        print('Column added')
    except Exception as e:
        print(f'Error: {e}')
        db.session.rollback()