from abc import ABCMeta, abstractmethod

from user.domain.user import User


class IUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError
    


