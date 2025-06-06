# gateway/shared/logging_config.py

import logging, sys
from logging.handlers import WatchedFileHandler

def configure_logging(log_file: str):
    """
    - 외부 cron 스크립트(log_rotate.sh)와 호환되는 WatchedFileHandler 사용
    - 탭(\t) 구분 포맷으로 asctime, levelname, message 기록
    """
    fmt = logging.Formatter(
        "%(asctime)s\t%(levelname)s\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1) 파일 핸들러 (외부에서 파일을 비워도 자동 재열기)
    fh = WatchedFileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)

    # 2) 콘솔 핸들러
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)

    # 3) 루트 로거 설정
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(fh)
    root.addHandler(ch)
