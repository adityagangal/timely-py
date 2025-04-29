# timely-py

This is the Python implementation of my timely-node backend. This porting is being done to ensure code can be easily maintained and understood by future maintainers. Partly to speed-up development because Python Supremacy!

This version uses Python | Fast-API | Beanie - Pydantic - Motor | MongoDB. 

The Android Front-End of the app is not uploaded because a few keys are present in my code, I don't feel comfortable posting them to github yet. :')


The other repo is present at [timely-node-mongo](https://github.com/RishiTiku/timely-node-mongo) and at [timely-node](https://github.com/RishiTiku/timely-node). I am sorry the first version is private because of keys present in testing and for them to be synced across devices, we directly used github with privacy.

The most challenging part of this project has been the schema design. Having conquered it, the rest of the development was easy. 


## Intermediate mini victories
### Love making my app faster for best UX
![image](https://github.com/user-attachments/assets/26dabfb2-f181-4b63-a6d9-635475d4fab6)

0-1 ms per query... I'd love to keep it that way!

### The Mongo Schema Design
Schema design for this application has been a crucial part of its speed and ultimately its scalablity. It took 3 weeks and 4 iterations to make a Mongo friendly denormalised schema.
![image](https://github.com/user-attachments/assets/63e14450-69a8-4a77-8733-fbf2769bf333)

