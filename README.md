# ConcoleRayTracing
![goursat](https://user-images.githubusercontent.com/95490512/199304113-1ba1afa2-599d-4413-9f5c-e42571aeacc6.png)
 RTX that I can afford

Код получился ни капли не оптимизированным и нарушает некоторые принципы SOLID, хоть я и старался этого не допускать как минимум класс DrawFrames можно разделить на RenderFrames и собственно DrawFrames.
Что касается производительности, то я на 80% уверен что все дело в этих трех строчках:
self.screen[i + j * self.width] = pixel
и 
for symbol in self.screen:
   frame += symbol
а именно в питоновском списке и строках.
Из-за чего даже когда не производится никаких вычислений, программа выдает в лучшем случае 8 фпс(Весьма неутешительный результат).
Я уверен, что все решается банальным numpy, но эту работу я хочу оставить на вас)
