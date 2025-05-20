## MongoDB 데이터 수동 로드

개발 환경에서 `product.json`과 `brand.json`을 수동으로 임포트하려면, 다음 명령을 실행하세요:

```bash
# Product 데이터 로드
docker exec -it mongodb_product \
  mongoimport \
    --uri "mongodb://root:mongodb_product@mongodb_product:27017/product?authSource=admin" \
    --collection product \
    --file ./data/product.json \
    --jsonArray \
    --drop

# Brand 데이터 로드
docker exec -it mongodb_brand \
  mongoimport \
    --uri "mongodb://root:mongodb_brand@mongodb_brand:27017/brand?authSource=admin" \
    --collection brand \
    --file ./data/brand.json \
    --jsonArray \
    --drop
