import time, os
from typing import Dict, Any

from Tea.exceptions import TeaException
from Tea.request import TeaRequest
from alibabacloud_tea_util import models as util_models
# from opensearch.V3_cases.doc_search.BaseRequest import Config, Client
from BaseRequest import Config, Client


class LLMSearch:
    def __init__(self, config: Config):
        self.Clients = Client(config=config)
        self.runtime = util_models.RuntimeOptions(
            connect_timeout=10000,
            read_timeout=10000,
            autoretry=False,
            ignore_ssl=False,
            max_idle_conns=50,
            max_attempts=3
        )
        self.header = {}


    def searchDoc(self, app_name: str,body:Dict, query_params: dict={}) -> Dict[str, Any]:
        try:
            response = self.Clients._request(method="POST", pathname=f'/v3/openapi/apps/{app_name}/actions/knowledge-search',
                                             query=query_params, headers=self.header, body=body, runtime=self.runtime)
            return response
        except TeaException as e:
            print(e)

class LLMDocumentPush:
    def __init__(self, config: Config):
        self.Clients = Client(config=config)
        self.runtime = util_models.RuntimeOptions(
            connect_timeout=10000,
            read_timeout=10000,
            autoretry=False,
            ignore_ssl=False,
            max_idle_conns=50,
            max_attempts=3
        )
        self.header = {}

    def docBulk(self, app_name: str,doc_content: list) -> Dict[str, Any]:
        try:
            response = self.Clients._request(method="POST",
                                             pathname=f'/v3/openapi/apps/{app_name}/actions/knowledge-bulk',
                                             query={}, headers=self.header,
                                             body=doc_content, runtime=self.runtime)
            return response
        except Exception as e:
            print(e)


def search_llm(app_name, ops, question):

    # --------------- Search for documents ---------------

    docQuery = {
            "question": {
                "text": question, 
                "type": "TEXT",
                "session": 2,
                # "content": "Legal Agreement Form.pdf"
            },
            "options": {
                "retrieve": {
                    "doc": {
                        "disable": False, # Specifies whether to disable the document retrieval feature. Default value: false. 
                        "filter": '', # Filters documents based on the specified category during document retrieval. By default, this parameter is left empty.
                        "sf": 1.3,    # The threshold of vector relevance for document retrieval. Default value: 1.3. The greater the value is, the less relevant the retrieved documents are.
                        "top_n": 5,    # The number of documents to be retrieved. Default value: 5. Valid values: (0,50].
                        "formula" : "", # By default, documents are retrieved based on vector similarity.
                        # "rerank_size" : 5, # The number of documents to be fine sorted. By default, you do not need to specify this parameter, and the system determines the number of documents to be fine sorted.
                        "operator":"AND"   # The operator between text tokens. In this example, the OR operator is used between text tokens when text documents are retrieved. Default value: AND.                                  
                    },
                    "entry": {
                        "disable": False, # Specifies whether to disable the intervention data retrieval feature. Default value: false. 
                        "sf": 0.3 # The vector relevance for intervention data retrieval. Default value: 0.3.
                    },
                },
                "chat": {
                    "stream" : False, # Specifies whether to enable HTTP chunked transfer encoding. Default value: false. 
                    "disable" : False, # specifies whether to disable the chat model. Default value: false. 
                    "model" : "opensearch-llama2-13b", # The LLM model. Valid values: Qwen and opensearch-llama2-13b.
                    "prompt_config": {
                        "attitude": "normal",
                        "rule": "detailed",
                        "noanswer": "sorry",
                        "language": "English",
                        "role": True,
                        "role_name": "AI Assistant"
                        # "out_format": "text"
                    }
                },
            }}

    res1 = ops.searchDoc(app_name=app_name, body=docQuery)
    # print("ANSWER ", res1["body"]["result"]["data"][0]["answer"])

    return res1["body"]["result"]["data"][0]["answer"]
    # print(res1)

def push_doc(app_name, ops):
    document = [
        {
            "fields": {
                "id": "1",
                "title": "Benefits",
                "url": "https://help.aliyun.com/document_detail/464900.html",
                "content": "Industry Algorithm Edition: Intelligence: Industry Algorithm Edition provides rich built-in and customized algorithm models and introduces industry retrieval and sorting algorithms based on the search needs of different industries. This way, optimal search results are ensured. Flexibility and customization: Industry Algorithm Edition allows you to customize configurations such as algorithm models, application schema, data processing, query analysis, and sorting to meet personalized search requirements. This improves the click-through rate of search results, accelerates service iteration, and greatly shortens the rollout cycle. Security and stability: O&M services are available on a 24/7 basis. You can get technical support by submitting tickets online or using the telephone. A series of complete fault emergency response mechanisms are provided, such as fault monitoring, automatic alerting, and rapid troubleshooting. AccessKey IDs and AccessKey secrets assigned by Alibaba Cloud control permissions to access OpenSearch. This ensures data security by isolating data of different users. Multiple copies of data are backed up to implement data redundancy, which ensures data security. Auto scaling: The auto scaling capability allows you to scale up or down the resources based on your needs. Rich extended features: OpenSearch supports a variety of extended search features, such as top searches, hints, drop-down suggestions, and report statistics. This helps you view and analyze search results. Out-of-the-box service: You do not need to deploy or perform O&M operations on clusters before you access OpenSearch. High-performance Search Edition: High throughput: A single table supports tens of thousands of write transactions per second (TPS) and data updates within seconds. Security and stability: O&M services are available on a 24/7 basis. You can get technical support by submitting tickets online or using the telephone. A series of complete fault emergency response mechanisms are provided, such as fault monitoring, automatic alerting, and rapid troubleshooting. AccessKey IDs and AccessKey secrets assigned by Alibaba Cloud control permissions to access OpenSearch. This ensures data security by isolating data of different users. Multiple copies of data are backed up to implement data redundancy, which ensures data security. Auto scaling: The auto scaling capability allows you to scale up or down the resources based on your needs. Out-of-the-box service: You do not need to deploy or perform O&M operations on clusters before you access OpenSearch. Vector Search Edition: Stability: The underlying layer of Vector Search Edition is developed by using the C++ programming language. After more than ten years of development, Vector Search Edition provides stable search services for various core business systems. Vector Search Edition is suitable for core search scenarios that require high stability. High efficiency: Vector Search Edition provides a distributed search engine that allows you to retrieve large amounts of data. Vector Search Edition supports real-time data updates within seconds. Therefore, Vector Search Edition is applicable to query and search scenarios that are time-sensitive. Cost-effectiveness: Vector Search Edition supports multiple policies for index compression and multi-value index loading tests. You can use Vector Search Edition to meet your query requirements at low costs. Vector algorithm: Vector Search Edition supports vector searches for various types of unstructured data, such as voice data, images, videos, natural languages, and behavior data. SQL query: Vector Search Edition allows you to use SQL syntax and join tables online and provides a variety of built-in user-defined functions (UDFs) and function customization mechanisms to meet different requirements for data retrieval. To facilitate SQL development and testing, an SQL studio is integrated into the O&M system of Vector Search Edition. Retrieval Engine Edition: Stability: The underlying layer of Retrieval Engine Edition is developed by using the C++ programming language. After more than ten years of development, Retrieval Engine Edition provides stable search services for various core business systems. Retrieval Engine Edition is suitable for core search scenarios that require high stability. High efficiency: Retrieval Engine Edition provides a distributed search engine that allows you to retrieve large amounts of data. Retrieval Engine Edition supports real-time data updates within seconds. Therefore, Retrieval Engine Edition is suitable for query and search scenarios that are time-sensitive. Cost-effectiveness: Retrieval Engine Edition supports multiple policies for index compression and multi-value index loading tests. You can use Retrieval Engine Edition to meet your query requirements at low costs. Enriched features: Retrieval Engine Edition supports multiple types of analyzers and indexes and powerful query syntax. This service can meet your data retrieval requirements. Retrieval Engine Edition also supports plug-ins. This way, you can customize your own business logic. SQL query: Retrieval Engine Edition allows you to use SQL syntax and join tables online, and provides a variety of built-in UDFs and function customization mechanisms to meet different requirements for data retrieval. To facilitate SQL development and testing, an SQL studio will be integrated into the O&M system of Retrieval Engine Edition in later versions.",
                "category": "opensearch",
                "timestamp": 1691722088645,
                "score": 0.8821945219723084
            },
            "cmd": "ADD"
        },
        {
            "fields": {
                "id": "2",
                "title": "Scenarios",
                "url": "https://help.aliyun.com/document_detail/464901.html",
                "content": "Industry Algorithm Edition: Features: provides industry built-in capabilities such as semantic understanding and machine learning-based algorithms, and supports lightweight custom models and search guidance. This helps you build intelligent search services in a quick manner. <br/><img src=\"https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4685770861/p622804.png\" width=300>Business scenarios: intelligent searches in industries such as e-commerce, content communities, and games, and educational Q&A searches. Target customers: Industry Algorithm Edition is out-of-the-box and suitable for small and medium-sized enterprises and developers that have intelligent search requirements. High-performance Search Edition: Features: Deep optimization is performed for big data search performance. OpenSearch supports quick response within seconds and real-time queries, and provides a one-stop solution for you to build big data search services in various scenarios such as searches for orders, coupons, logistics, and insurance policies. <br/><img src=\"https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3685770861/p622799.png\" width=300>Business scenarios: searches for orders, coupons, logistics, and insurance policies. Target customers: High-performance Search Edition is out-of-the-box and suitable for small and medium-sized enterprises and developers that have high requirements for search performance. Vector Search Edition: Features: provides a large-scale distributed and high-performance vector search solution in Alibaba Cloud. Vector Search Edition supports multiple search algorithms to achieve a balance between precision and performance. Other features such as building index in streaming mode and instant queries are also supported. <br/><img src=\"https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4685770861/p622805.png\" width=300>Business scenarios: graph searches, audio or video searches, natural language processing (NLP) vector searches, and intelligent Q&A. Target customers: enterprises and developers that face large-scale vectors and require flexible development. Retrieval Engine Edition: Features: provides you with high-performance, low-cost, easy-to-use, and large-scale online search services. Retrieval Engine Edition supports customized development based on your business requirements and fast iteration of search algorithms. <br/><img src=\"https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4685770861/p622806.png\" width=300>Business scenarios: searches for enterprise information, tags, and financial research reports, and intelligent searches. Target customers: enterprises and developers that face a large amount of data and require flexible data development.",
                "category": "opensearch",
                "timestamp": 1691722088646,
                "score": 0.8993507402088953
            },
            "cmd": "ADD"
        }
    ]

    # Delete a record.
    deletedocument = {"cmd": "DELETE", "fields": {"id": 2}}
    documents = document
    res5 = ops.docBulk(app_name=app_name, doc_content=documents)
    return res5
    

if __name__ == "__main__":
    # Specify the endpoint of the OpenSearch API. The value does not contain the http:// prefix.
    endpoint = "opensearch-ap-southeast-1.aliyuncs.com"

    # Specify the request protocol. Valid values: HTTPS and HTTP.
    endpoint_protocol = "HTTP"

    # Specify your AccessKey pair.
    # Obtain the AccessKey ID and AccessKey secret from environment variables. 
    # You must configure environment variables before you run this code. For more information, see the "Configure environment variables" section of this topic.
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

    # Specify the authentication method. Default value: access_key. A value of sts indicates authentication based on Resource Access Management (RAM) and Security Token Service (STS).
    # Valid values: sts and access_key.
    auth_type = "access_key"

    # If you use authentication based on RAM and STS, you must specify the security_token parameter. You can call the AssumeRole operation of Alibaba Cloud RAM to obtain an STS token.
    security_token =  "<security_token>"

    # Specify common request parameters.
    # The type and security_token parameters are required only if you use the SDK as a RAM user.
    Configs = Config(endpoint=endpoint, access_key_id=access_key_id, access_key_secret=access_key_secret,
                     security_token=security_token, type=auth_type, protocol=endpoint_protocol)

    # Create an OpenSearch instance.
    app_name = "agile_LLM"


    # print(res1)
    while True:
        print("\t\tWELCOME TO CHAT")
        print("1. Q&A Feature: ")
        print("2. Push Document: ")

        choice = int(input("Option: "))
        if choice ==1:
            ops = LLMSearch(Configs)
            print("What can I help?")
            while True:
                question = input("\n")

                if not question.lower() == 'exit':
                    print("\n\nResponse: ", search_llm(app_name, ops, question))
                else:
                    break


        elif choice == 2:
            ops = LLMDocumentPush(Configs)
            print("STATUS: ", push_doc(app_name, ops))
        else:
            break

