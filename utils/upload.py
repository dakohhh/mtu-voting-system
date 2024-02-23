import os
from pprint import pprint
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
from typing import Union, Any

load_dotenv()




cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),

  api_key = os.getenv("CLOUDINARY_API_KEY"), 

  api_secret = os.getenv("CLOUDINARY_API_SECRET"),

  secure = True
)



class Upload():

	def __init__(self, private_name, file:Union[str, Any], file_name):

		self.private_name = private_name

		self.file = file

		self.file_name = file_name

	def handle_upload(self) -> dict:

		metadata = cloudinary.uploader.upload(
			self.file, 
			public_id=f"{self.private_name}/{self.file_name}")

		return metadata


	async def handle_delete(self, name:str):

		public_ids = ["them_wisdom.jpg"]
		image_delete_result = cloudinary.api.delete_resources(public_ids, resource_type="image", type="upload")
		print(image_delete_result)

		result = cloudinary.api.delete_resources(public_ids, resource_type="video", type="upload")

		print(result)

	

class SecuritySystemUpload(Upload):

	private_name = "security_campus"

	def __init__(self, file:Union[str, Any], file_name:str):

		super().__init__(self.private_name, file, file_name)




if __name__ == "__main__":

	path = os.path.join(os.getcwd(), "upload_data/image.jpg")

	uploader = SecuritySystemUpload(path, "them_wisdom")

	pprint(uploader.handle_upload())

























