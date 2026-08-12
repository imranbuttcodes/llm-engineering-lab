from langchain_core.runnables import RunnableAssign
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnableLambda

chain = RunnableAssign(

    RunnableParallel({

        "square": RunnableLambda(
            lambda x: x["number"] ** 2
        ),

        'cube': RunnableLambda(
            lambda x: x['number'] ** 3
        )

    })

)

result = chain.invoke({

    "number":5

})

print(result)