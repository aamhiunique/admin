npm install -g serverless

sls -v

sls create --template aws-python

echo "Enter AWS Access Key: "
read AWSKey

echo "Enter AWS SECRET: "
read SECRETKey

serverless config credentials --provider aws --key $AWSKey --secret $SECRETKey

sls deploy 

