import os
from pprint import pprint
import shutil
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
from typing import Union, Any

from fastapi import UploadFile

load_dotenv()




cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),

  api_key = os.getenv("CLOUDINARY_API_KEY"), 

  api_secret = os.getenv("CLOUDINARY_API_SECRET"),

  secure = True
)



class Upload():

	def __init__(self, private_name, file_name):

		self.private_name = private_name

		self.file_name = file_name
		

	def handle_upload(self, file:Union[UploadFile, Any]) -> dict:

		metadata = cloudinary.uploader.upload(
			file.file, 
			folder=self.private_name,
			resource_type="auto",
			public_id=f"{self.private_name}/{self.file_name}"
		)
		
		return metadata


	async def handle_delete(self):

		public_ids = [f"{self.private_name}/{self.private_name}/{self.file_name}"]

		image_delete_result = cloudinary.api.delete_resources(
			public_ids, 
			resource_type="image", 
			type="upload"
		)

		return image_delete_result

	

class MTUVoteUpload(Upload):

	private_name = "mtu_vote"

	def __init__(self, file_name:str):

		super().__init__(self.private_name, file_name)




if __name__ == "__main__":

	path = os.path.join(os.getcwd(), "./picture.png")

	uploader = MTUVoteUpload(path)

	pprint(uploader.handle_upload(path))