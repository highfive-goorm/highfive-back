#!/bin/bash
# 초기 빈 데이터베이스에만 실행됩니다
mongoimport \
  --uri "mongodb://root:mongodb_product@mongodb_product:27017/product?authSource=admin" \
  --collection product \
  --file /docker-entrypoint-initdb.d/product.json \
  --jsonArray \
  --drop