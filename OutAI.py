def get_completion(user_input):
    from google.cloud import storage
    import os
    import time
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\trial-1-416716-f084dc92a348.json"
    with open(r"C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\input.txt", 'w') as file:
        file.write(user_input)

    def upload_file(bucket_name, source_file_name, destination_file_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_file_name)
        blob.upload_from_filename(source_file_name)
        return True

    upload_file('new-bucket89',r"C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\input.txt",'input.txt')
    print("Uploaded")
    time.sleep(35)

    def download_file(bucket_name, file_name, destination_file_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(destination_file_name)
        return True

    download_file('new-bucket89', 'output.txt', r"C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\output.txt")
        # Open the input.txt file and read its contents
    with open(r"C:\Users\annad\OneDrive\Documents\Programmes\Resume Parser\output.txt", 'r') as file:
        input_text = file.read()
        print("Downloaded")
        return input_text