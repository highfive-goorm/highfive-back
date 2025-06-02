#!/bin/bash
mongoimport \
  --uri "mongodb://root:mongodb_brand@mongodb_brand:27017/brand?authSource=admin" \
  --collection brand \
  --file /docker-entrypoint-initdb.d/brand.json \
  --jsonArray \
  --drop