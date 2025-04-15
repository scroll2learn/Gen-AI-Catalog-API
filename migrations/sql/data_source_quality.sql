UPDATE catalogdb.data_source
SET data_src_quality = 50 + FLOOR(RANDOM() * 51);