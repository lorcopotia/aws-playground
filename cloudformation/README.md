# Encendido y apagado de instancias EC2 utilizando CloudFormation

1. Política IAM para EC2

```
aws iam create-policy \
  --policy-name EC2StartStopPolicy \
  --policy-document '{
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "ec2:StartInstances",
                  "ec2:StopInstances",
                  "ec2:DescribeInstances"
              ],
              "Resource": "*"
          }
      ]
  }'
```

2. Crear el rol de Lambda

```
aws iam create-role \
  --role-name LambdaEC2StartStopRole \
  --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Principal": {
                  "Service": "lambda.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
          }
      ]
  }'
```

3. Adjuntar las políticas al rol:

```bash
aws iam attach-role-policy --role-name LambdaEC2StartStopRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy --role-name LambdaEC2StartStopRole --policy-arn arn:aws:iam::ACCOUNT_ID:policy/EC2StartStopPolicy
```

4. Crear la función Lambda. Utilizando el fichero `manage-instances.py` que contiene la función que nos permitirá filtrar las máquinas y ejecutar la tarea.

5. Subimos el fichero:

```
# Comprimimos el fichero para poderlo subir
zip manage_instances manage-instances.py

aws lambda create-function \
  --function-name ManageWorkstationInstances \
  --runtime python3.8 \
  --role arn:aws:iam::666423461342:role/LambdaEC2StartStopRole \
  --handler manage_instances.lambda_handler \
  --zip-file fileb://manage_instances.zip

```

6. Creamos los eventos en EventBridge

```
aws events put-rule \
  --name "StartWorkstationInstances" \
  --schedule-expression "cron(0 7 * * ? *)"

```

7. Para asociar el evento con la regla de Lambda utilizamos el JSON `target-start.json` y ejecutamos el comando:

```bash
aws events put-targets --cli-input-json file://target-start.json
```


- Lo mismo para asociar la regla con Lambda que define el evento de acción de apagado. 

```bash
aws events put-targets --cli-input-json file://target-stop.json
```

8. Invocar la función manualmente:

```
aws lambda invoke   --function-name ManageWorkstationInstances   --payload '{"action": "start"}'   --cli-binary-format  raw-in-base64-out response.json
```
