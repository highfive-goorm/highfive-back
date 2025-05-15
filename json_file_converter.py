import os
import json

DATA_DIR = './data'
OUTPUT_DIR = './mongo-init'

# 변환할 파일 목록
FILES = [
    'promotion.json'
]

def convert_json_files():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in FILES:
        input_path = os.path.join(DATA_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(input_path, 'r', encoding='utf-8') as infile:
            # 각 줄을 개별 JSON 객체로 간주하여 배열로 묶음
            data = [json.loads(line.strip()) for line in infile if line.strip()]

        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

        print(f'✅ {filename} 변환 완료 → {output_path}')


if __name__ == '__main__':
    convert_json_files()
    print('\n🎉 모든 파일 변환 완료!')
