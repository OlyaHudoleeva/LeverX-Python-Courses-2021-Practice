import re
from functools import total_ordering


@total_ordering
class Version:
    PATCH_DETAILS = [
        "alpha",
        "alpha.beta",
        "beta",
        "rc",
        ""
    ]

    def __init__(self, version):
        """
        В методе происходит следующая токенизация:

        1. major - основная версия продукта
        2. minor - младшая версия продукта
        3. patch - версия мелких изменений продукта

        patch в свою очередь разбивается на:

        1. patch_version - номер версии мелких изменений
        2. patch_symbol - буква в качестве младшей версии исправленной ошибки
        3. patch_detail - стадия разработки (alpha, beta и т.д.)
        4. patch_subversion - подверсия деталей разработки патча

        На примере версии 1.0.10-alpha.beta:

        1. major - 1
        2. minor - 0
        3. patch - 10-alpha.beta
        4. patch_version - 10
        5. patch_symbol - нет
        6. patch_detail - alpha.beta
        7. patch_subversion - beta

        На примере версии 1.0.1b:

        1. major - 1
        2. minor - 0
        3. patch - 1b
        4. patch_version - 1
        5. patch_symbol - b
        6. patch_detail - нет
        7. patch_subversion - нет
        """

        major, minor, patch = version.split(".", maxsplit=2)
        self.major = int(major)
        self.minor = int(minor)
        patch_split = patch.split("-")
        self.patch_version = re.findall(r'[0-9]+', patch_split[0])[0]
        symbols = re.findall(r'[a-z]+', patch_split[0])
        self.patch_symbol = "" if symbols == [] else symbols[0]
        self.patch_detail = "" if len(patch_split) == 1 else patch_split[1]
        patch_subversion = re.findall(r'[0-9]+', self.patch_detail)
        if patch_subversion:
            self.patch_detail = self.patch_detail.split(".")[0]
            self.patch_subversion = int(patch_subversion[0])
        else:
            # -1 однозначно меньше любой валидной подверсии патча
            self.patch_subversion = -1

    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch_version != other.patch_version:
            return self.patch_version < other.patch_version
        if self.patch_symbol != other.patch_symbol:
            return self.patch_symbol < other.patch_symbol
        if self.PATCH_DETAILS.index(self.patch_detail) != self.PATCH_DETAILS.index(other.patch_detail):
            return self.PATCH_DETAILS.index(self.patch_detail) < self.PATCH_DETAILS.index(other.patch_detail)
        if self.patch_subversion != other.patch_subversion:
            return self.patch_subversion < other.patch_subversion

        return False

    def __gt__(self, other):
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        if self.patch_version != other.patch_version:
            return self.patch_version > other.patch_version
        if self.patch_symbol != other.patch_symbol:
            return self.patch_symbol > other.patch_symbol
        if self.PATCH_DETAILS.index(self.patch_detail) != self.PATCH_DETAILS.index(other.patch_detail):
            return self.PATCH_DETAILS.index(self.patch_detail) > self.PATCH_DETAILS.index(other.patch_detail)
        if self.patch_subversion != other.patch_subversion:
            return self.patch_subversion > other.patch_subversion

        return False

    def __eq__(self, other):
        if self.major != other.major:
            return False
        if self.minor != other.minor:
            return False
        if self.patch_version != other.patch_version:
            return False
        if self.patch_symbol != other.patch_symbol:
            return False
        if self.PATCH_DETAILS.index(self.patch_detail) != self.PATCH_DETAILS.index(other.patch_detail):
            return False
        if self.patch_subversion != other.patch_subversion:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return ".".join([str(self.major), str(self.minor), str(self.patch_version)]) + "-".join(
            [self.patch_symbol, self.patch_detail]) + "." + self.patch_subversion

v1 = Version("1.0.10-alpha.beta")
v2 = Version("1.0.1b")

def main():
    # 0-alpha < 0-alpha.1 < 0-alpha.beta < 0-beta < 0-beta.2 < 0-beta.11 < 0-rc.1 < 0 < 0b < 0c < 1
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        print(version_1, version_2)
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
