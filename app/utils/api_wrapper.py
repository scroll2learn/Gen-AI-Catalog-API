from app.utils.request_wrapper import RequestWrapper

from app.core.config import Config


class APIWrapper:

    def __init__(self):
        self.request_wrapper = RequestWrapper(base_url=Config.AUTHOR_DATA_ENDPOINT)

    async def get_file_process(
            self,
            name: str = 'Test Source 1',
            source_file_path: str = "s3a://bighammer-sample-data-development/01_DBC.csv",
            lake_zone_id: int = 401,
            data_src_status_cd: int = 703,
        ):
        data = {
            'name': name,
            'source_file_path': source_file_path,
            'lake_zone_id': lake_zone_id,
            'data_src_status_cd': data_src_status_cd,
        }
        fmt_endpoint = f"api/v1/author_data/process-file"
        response = await self.request_wrapper.call_api(endpoint=fmt_endpoint, method="post", data=data)
        return response

    async def get_sample_data(self, source_file_path: str, data_src_key: str, num_rows: int = 10):
        fmt_endpoint = f"api/v1/author_data/get-sample-data?source_file_path={source_file_path}&data_src_key={data_src_key}&num_rows={num_rows}"
        response = await self.request_wrapper.call_api(endpoint=fmt_endpoint, method="get")
        return response['sample_data']
    
    async def get_field_properties(self, source_file_path: str, data_src_key: str, field_name: str):
        fmt_endpoint = f"api/v1/author_data/get-field-properties?source_file_path={source_file_path}&data_src_key={data_src_key}&field_name={field_name}"
        response = await self.request_wrapper.call_api(endpoint=fmt_endpoint, method="get")
        print(response)
        print("Above is response")
        return response

# test = APIWrapper()
# asyncio.run(test.get_file_process())
