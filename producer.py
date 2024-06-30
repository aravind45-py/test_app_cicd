from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import boto3,time

# Function to fetch AWS credentials using boto3
def get_aws_credentials():
    session = boto3.Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()
    return current_credentials.access_key, current_credentials.secret_key, current_credentials.token

# Function to create topic if it doesn't exist
def create_topic(admin_client, topic_name, num_partitions=1, replication_factor=1):
    topic_list = [NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    fs = admin_client.create_topics(topic_list)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"Topic {topic} created successfully")
        except Exception as e:
            if 'TopicAlreadyExistsError' in str(e):
                print(f"Topic {topic} already exists")
            else:
                print(f"Failed to create topic {topic}: {e}")

# Fetch AWS credentials
aws_access_key, aws_secret_key, aws_session_token = get_aws_credentials()
bootstrap_servers = '<your-bootstrap-brokers>'

# Configure AdminClient for topic creation
admin_conf = {
    'bootstrap.servers': bootstrap_servers,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'AWS_MSK_IAM',
    'sasl.username': aws_access_key,
    'sasl.password': aws_secret_key,
    'sasl.oauthbearer.token': aws_session_token
}

# Create AdminClient
admin_client = AdminClient(admin_conf)

# Topic name
topic_name = 'demo-topic'

# Check if topic exists and create if not
existing_topics = admin_client.list_topics().topics
if topic_name not in existing_topics:
    create_topic(admin_client, topic_name)
else:
    print(f"Topic {topic_name} already exists")

# Configure the producer
producer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'AWS_MSK_IAM',
    'sasl.username': aws_access_key,
    'sasl.password': aws_secret_key,
    'sasl.oauthbearer.token': aws_session_token
}

# Create the producer
producer = Producer(**producer_conf)

# Produce a message
for i in range(10):
    producer.produce(topic_name,value='value')
    time.sleep(1)
producer.flush()
print("Message produced successfully")
