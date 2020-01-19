import kfp
import kfp.components as comp
import kfp.dsl as dsl

ner_op = comp.load_component_from_url('https://raw.githubusercontent.com/mereszeta/kubeflow-workflows/master/ner.yaml')
help(ner_op)
sentiment_op = comp.load_component_from_url(
    'https://raw.githubusercontent.com/mereszeta/kubeflow-workflows/master/sentiment.yaml')
help(sentiment_op)


def echo2_op(text1, text2):
    return dsl.ContainerOp(
        name='echo',
        image='library/bash:4.4.23',
        command=['sh', '-c'],
        arguments=['echo "Ner: $0"; echo "Sentiment: $1"', text1, text2]
    )


@dsl.pipeline(
    name='Nlp kubeflow pipeline',
    description='A pipeline which finds named entities and calculates sentiment'
)
def text_transformation_pipeline(bucketName, fileCount):
    ner = ner_op(bucketName, fileCount)
    sentiment = sentiment_op(bucketName, fileCount)
    echo_task = echo2_op(ner.output, sentiment.output)
