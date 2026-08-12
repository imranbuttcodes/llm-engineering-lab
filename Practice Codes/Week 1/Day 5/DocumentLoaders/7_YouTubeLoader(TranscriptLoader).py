from langchain_community.document_loaders import YoutubeLoader

loader = YoutubeLoader.from_youtube_url(
    'https://www.youtube.com/watch?v=0QzopZ78w9M',

)

docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)