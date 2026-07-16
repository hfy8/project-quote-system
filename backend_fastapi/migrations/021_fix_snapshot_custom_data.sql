-- 一次性数据修正: 回填 version_snapshots 里 is_custom=true 物料的快照字段
-- 原因: _create_version_snapshot 旧版本没处理 is_custom 分支, 自制件 material=None
--       导致所有字段被存成 None/0, 版本对比时被算成 0 元
-- 修复后 v1.4.69: _create_version_snapshot 会正确写入
DO $$
DECLARE
    vs_rec RECORD;
    mod_rec jsonb;
    mat_rec jsonb;
    new_mat jsonb;
    new_materials jsonb;
    new_mod jsonb;
    new_modules jsonb;
    i int;
    j int;
    n_mods int;
    n_mats int;
BEGIN
    FOR vs_rec IN SELECT id, snapshot_data FROM version_snapshots LOOP
        new_modules := '[]'::jsonb;
        n_mods := jsonb_array_length(vs_rec.snapshot_data::jsonb->'modules');
        FOR i IN 0..n_mods-1 LOOP
            mod_rec := (vs_rec.snapshot_data::jsonb->'modules'->>i)::jsonb;
            new_materials := '[]'::jsonb;
            n_mats := jsonb_array_length(mod_rec->'materials');
            FOR j IN 0..n_mats-1 LOOP
                mat_rec := (mod_rec->'materials'->>j)::jsonb;
                new_mat := mat_rec;
                IF (mat_rec->>'is_custom')::boolean = true THEN
                    IF COALESCE((mat_rec->>'unit_price')::numeric, 0) = 0 THEN
                        new_mat := jsonb_set(new_mat, '{unit_price}',
                            to_jsonb(COALESCE(
                                (mat_rec->'custom_data'->>'unit_price')::numeric,
                                (mat_rec->>'unit_price_override')::numeric, 0))
                        );
                    END IF;
                    IF mat_rec->>'name' IS NULL AND mat_rec->'custom_data'->>'name' IS NOT NULL THEN
                        new_mat := jsonb_set(new_mat, '{name}', to_jsonb(mat_rec->'custom_data'->>'name'));
                    END IF;
                    IF mat_rec->>'brand' IS NULL AND mat_rec->'custom_data'->>'brand' IS NOT NULL THEN
                        new_mat := jsonb_set(new_mat, '{brand}', to_jsonb(mat_rec->'custom_data'->>'brand'));
                    END IF;
                    IF mat_rec->>'spec' IS NULL AND mat_rec->'custom_data'->>'spec' IS NOT NULL THEN
                        new_mat := jsonb_set(new_mat, '{spec}', to_jsonb(mat_rec->'custom_data'->>'spec'));
                    END IF;
                END IF;
                new_materials := new_materials || jsonb_build_array(new_mat);
            END LOOP;
            new_mod := jsonb_set(mod_rec, '{materials}', new_materials);
            new_modules := new_modules || jsonb_build_array(new_mod);
        END LOOP;
        UPDATE version_snapshots SET snapshot_data = jsonb_set(vs_rec.snapshot_data::jsonb, '{modules}', new_modules)::text
        WHERE id = vs_rec.id;
    END LOOP;
END $$;
