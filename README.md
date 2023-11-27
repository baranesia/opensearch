# opensearch
To create intelligent search, OpenSearch is a one-stop Solution as a Service (SaaS) technology that is applicable to industry-specific search scenarios and provides a dedicated conversational search service for enterprises. There are 5 edition of Open Search and we are going to use LLM-Based Conversational Search Edition.

LLM-Based Conversational Search Edition can automatically generate conversational search results in various formats such as texts, reference images, and reference links based on business data. The conversational search service is intelligent and high-quality.

Purchase Open Search by accessing https://common-buy-intl.alibabacloud.com/?spm=opensearchspma.knowledge-instances.0.0.7bab6bd6DJt9Yf&commodityCode=opensearch_openknowledge_public_intl.

In ECS or local library, install the required libraries

pip install alibabacloud_tea_util 
pip install alibabacloud_opensearch_util
pip install alibabacloud_credentials
Create environmental variable for the Alibaba Cloud Access Key and Secret.

export ALIBABA_CLOUD_ACCESS_KEY_ID=<access_key_id> 
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=<access_key_secret>
Go to the existing directory then run
cd llm-python
python3 app.py
