# -*- coding: utf-8 -*-
# @Author   : linshukai
# @Date     : 2022/5/21
# @Description  :   logging模块使用

import logging

from logging import FileHandler, StreamHandler
from logging import Formatter


def init_logger():
    # 命名记录器（每个使用日志记录的模块使用模块级的日志记录器）
    logger = logging.getLogger(__name__)
    # 记录器设置的名称为模块文件的名称，能够直观的显示记录事件的位置

    logger.setLevel("DEBUG")

    fm = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                   "%Y-%m-%d %H:%M:%S")

    fh = FileHandler("example.log")
    fh.setLevel("WARNING")
    fh.setFormatter(fm)

    ch = StreamHandler()
    ch.setLevel("DEBUG")
    ch.setFormatter(fm)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


if __name__ == "__main__":
    logger = init_logger()
    logger.debug("DEBUG TEST")
    logger.info("INFO TEST")
    logger.warning("WARNING TEST")
    logger.error("ERROR TEST")
    logger.critical("CRITICAL TEST")
    logger.log(2, "DEBUG TEST")
    try:
        a = 1/0

    except Exception as e:
        logger.exception(f"EXCEPTION TEST: {str(e)}")

