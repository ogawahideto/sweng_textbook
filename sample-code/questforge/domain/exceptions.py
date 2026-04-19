"""ドメイン層固有の例外クラス

ビジネスルールに違反した場合などに投げられる例外を定義します。
"""

class DomainError(Exception):
    """QuestForgeドメインの基底例外クラス"""
    pass

class InvalidQuestStateError(DomainError):
    """クエストのステータス遷移が不正な場合に投げられる例外"""
    pass

class InsufficientLevelError(DomainError):
    """レベルが不足している場合に投げられる例外"""
    pass

class RepositoryError(DomainError):
    """リポジトリ操作でエラーが発生した場合に投げられる例外"""
    pass
