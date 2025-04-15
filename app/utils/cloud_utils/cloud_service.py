from abc import ABC, abstractmethod

class CloudService(ABC):

    @abstractmethod
    async def copy_file_to_object_storage(self):
        pass
