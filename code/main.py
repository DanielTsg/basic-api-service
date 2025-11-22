import pandas as pd
from azureml.core import Workspace, Dataset, Datastore
import os
from dotenv import load_dotenv

subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group = os.getenv('AZURE_RESOURCE_GROUP')
workspace_name = os.getenv('AZURE_WORKSPACE_NAME')

# 连接 workspace
workspace = Workspace(subscription_id, resource_group, workspace_name)

# 新建 DataFrame
data = {'col1': [1, 2], 'col2': ['A', 'B']}
df = pd.DataFrame(data)

# 保存为 CSV 文件
df.to_csv('my_table.csv', index=False)

# 获取默认 datastore
datastore = workspace.get_default_datastore()

# 上传 CSV 文件到 datastore
datastore.upload_files(['my_table.csv'], target_path='my_data/', overwrite=True)

# 注册为 AzureML Dataset
dataset = Dataset.Tabular.from_delimited_files(path=(datastore, 'my_data/my_table.csv'))
dataset = dataset.register(workspace=workspace, name='MyNewTable', create_new_version=True)

print("上传并注册完成")