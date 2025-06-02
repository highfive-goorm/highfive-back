#!/bin/bash
echo "==> Importing product.json into mydb.product"
mongoimport \
  --uri "mongodb://root:mongodb_product@localhost:27017/product \
  --collection products \
  --file /docker-entrypoint-initdb.d/product.json \
  --jsonArray