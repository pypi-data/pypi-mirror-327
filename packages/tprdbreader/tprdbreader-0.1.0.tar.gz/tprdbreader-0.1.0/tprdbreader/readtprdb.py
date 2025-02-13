from google.cloud import storage
import pandas as pd
import io

def readTPRDBtable_GCP(studies, ext, path, bucket_name, verbose=0):
    """
    Reads files from the given bucket that match the specified extension,
    under the given base path combined with each study subfolder.
    
    Parameters:
      studies (list): A list of study subfolder strings, e.g. ["BML12/Tables/", "AR20/Tables/"]
      ext (str): File extension pattern, e.g. "kd"
      path (str): The base path where the studies are stored.
      bucket_name (str): Name of the bucket. 
      verbose (int): If non-zero, prints the number of sessions and rows processed.
      
    Returns:
      A pandas DataFrame containing the concatenated data from the matching files.
    """
    # Initialize an anonymous client
    client = storage.Client.create_anonymous_client()

    # Get a bucket reference without triggering an API call that requires refreshing credentials
    bucket = client.bucket(bucket_name)

    df = pd.DataFrame()

    for study in studies:
        # Build the path for the study folder provided by the user
        prefix = f"{path}{study}"

        # List all blobs (files) under the study folder
        # Note: list_blobs() here should work if the objects are public.
        blobs = bucket.list_blobs(prefix=prefix)

        # Filter the blobs by the file extension
        files = [blob.name for blob in blobs if blob.name.endswith(ext)]

        if not files:
            print(f"No files found for study {study} with extension {ext}")
            continue

        # Fetch the file content and load it into a DataFrame
        dataframes = []
        for file in files:
            blob = bucket.blob(file)
            content = blob.download_as_text()  # Download the content as text
            dataframes.append(pd.read_csv(io.StringIO(content), sep="\t"))

        # Print the number of sessions and rows
        if verbose:
            row_count = sum(len(df.index) for df in dataframes)
            print(f"{study}\t#sessions: {len(dataframes)}\t{ext}:{row_count}")

        # Combine dataframes from all files
        dataframes.insert(0, df)
        df = pd.concat(dataframes, ignore_index=True)

    return df
