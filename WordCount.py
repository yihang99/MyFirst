import wordcloud
import turtle
import jieba
name = input("Please input file name (.txt):")
file = open(name, "r")
txt = file.read()
file.close()
c = wordcloud.WordCloud(font_path='msyh.ttc'.upper(), width=800, height = 800)
c.generate(' '.join(jieba.lcut(txt)))
c.to_file("WdCld.png")

#print(' '.join(jieba.lcut(txt)))
