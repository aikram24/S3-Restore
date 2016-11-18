# Ali Ikram
import boto3
import botocore
from botocore.exceptions import ClientError
# temp
import pprint
pp = pprint.PrettyPrinter(indent=4)

client = boto3.client('s3')
delete_object_dict = {}

class s3(object):
	def __init__(self, bucketName):
		self.bucketName = bucketName


	def get_bucket_list(self):
		bucket_List = []
		response = client.list_buckets()
		for v in response['Buckets']:
			bucket_List.append(v['Name'])
		return (self.get_bucket_info(bucket_List))


	def check_if_versioning(self):
		response = client.get_bucket_versioning(Bucket=self.bucketName)
		if 'Status' in response.keys():
			if response['Status'] == "Enabled":
				return True
		else: 
			return False

	def object_versions(self):
		response = client.list_object_versions(Bucket=self.bucketName)
		# pp.pprint(response)
		i = 0
		if 'DeleteMarkers' in response:
			for mark in response['DeleteMarkers']:
				i = i + 1
				print ("Version {}:\n-------\nLastModified: {} UTZ\nObject Key: {}\nVersionID: {}\n".format(i, mark['LastModified'], mark['Key'], mark['VersionId']))
				data = {'Version {}'.format(i) : [{'Key': mark['Key'], 'VersionID': mark['VersionId'], 'Time': mark['LastModified']}]}
				delete_object_dict.update(data)
		else:
			print "No delete marker found"
			exit()
		# for version in response['Versions']:
		# 	i = i +1
		# 	print ("Version {}:\n-------\nLastModified: {}\nVersionID: {}\nUTZ Time: {}".format(i, version['LastModified'], version['VersionId'], version['LastModified']))

	def delete_objects(self):
		user_input = raw_input('\nEnter Y to restore all delete markers \nEnter D to restore delete markers for a certain directory\nEnter F to restore a file\nEnter C to cancel the process\n')
		if str(user_input.lower()) == 'y':
			for obj in delete_object_dict.values():
				for v in obj:
					response = client.delete_objects(Bucket=self.bucketName, Delete={'Objects': [{'Key': "{}".format(v['Key']), 'VersionId': "{}".format(v['VersionID'])}], 'Quiet': True})
			print ('Delete Marker are restored for full bucket')

		elif str(user_input.lower()) == 'c':
			print ('exiting.....')
			exit()
		elif str(user_input.lower()) == 'd':
			dir_to_restore = raw_input("Enter the directory name to finish the loop enter exit: ")
			while dir_to_restore != 'exit':
				for obj in delete_object_dict.values():
					for v in obj:
						if dir_to_restore in v['Key']:
							response = client.delete_objects(Bucket=self.bucketName, Delete={'Objects': [{'Key': "{}".format(v['Key']), 'VersionId': "{}".format(v['VersionID'])}], 'Quiet': True})
						else:
							continue
				dir_to_restore = raw_input("Enter the directory name or to finish the loop enter exit: ")
			print ('Directory/Directories restored')
		elif str(user_input.lower()) == 'f':
			file_to_restore_key = raw_input("Enter the file key or exit to finish the loop: ")
			while file_to_restore_key.lower() != 'exit':
				file_to_restore_version = raw_input("Enter the v VersionID: ")
				response = client.delete_objects(Bucket=self.bucketName, Delete={'Objects': [{'Key': file_to_restore_key, 'VersionId': file_to_restore_version}], 'Quiet': True})
				file_to_restore_key = raw_input("Enter the file key or exit to finish the loop:: ")
			print ('file(s) restored')
	
	def get_bucket_info(self, bucket_List):
		if self.bucketName in bucket_List and self.check_if_versioning() == True:
			print("Bucket {} found and have version enabled".format(self.bucketName))
			self.object_versions()
			self.delete_objects()
			

		elif self.bucketName in bucket_List and self.check_if_versioning() == False:
			print ("Bucket {} found and have version disabled".format(self.bucketName))
		else:
			print ("{} name is not found in bucket list".format(self.bucketName))



