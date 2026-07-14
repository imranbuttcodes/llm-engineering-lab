from langchain_core.runnables import RunnablePick

pick = RunnablePick("name")

result = pick.invoke({

    "name":"Imran",

    "age":21,

    "city":"Lahore"

})

print(result)




from langchain_core.runnables import (
    RunnableAssign,
    RunnableParallel,
    RunnableLambda,
    RunnablePick
)

assign = RunnableAssign(

    RunnableParallel({

        "square": RunnableLambda(
            lambda x: x["number"] ** 2
        ),

        "cube": RunnableLambda(
            lambda x: x["number"] ** 3
        )

    })

)

pick = RunnablePick(["cube"])

chain = assign | pick

result = chain.invoke({

    "number":4

})

print(result)