import re
from abc import ABC, abstractmethod

class Corpus(ABC):
    """
    Corpus 基类，定义处理文本数据的基本接口。
    """
    def __init__(self, data: str, max_seq_len=1000):
        self.max_seq_len = max_seq_len
        # data = [dt[:1000] for dt in data]
        self.data = data  # 存储原始数据

    @abstractmethod
    def clean(self):
        """清洗数据"""

    @abstractmethod
    def get_samples(self, num_samples=5):
        """返回指定数量的文本样本"""

    def __len__(self):
        """返回数据的长度"""
        return len(self.data)

class SeeridiaChemistryNoteCorpus(Corpus):
    """
    https://github.com/Seeridia/Chemistry-Note
    """
    def clean(self):
        sections = []
        buffer = []

        for line in self.data.split('\n'):
            if re.match(r'^#{1,5}', line):
                if buffer:
                    sections.append('\n'.join(buffer).strip())
                    buffer = []
            buffer.append(line)

        if buffer:
            sections.append('\n'.join(buffer).strip())

        self.data = [re.sub(r'<img[^>]*>', '', section).strip()\
                      for section in sections]  # 删去html图片标签
    def get_samples(self, num_samples=5):
        """
        num samples <= 0 时返回所有样本
        """
        if num_samples > 0:
            return self.data[:num_samples]
        return self.data
