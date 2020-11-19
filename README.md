### tl;dr;

Just run `./run.sh`, proceed to `localhost:5000` and enter your name.

### Description

Simple project which wraps russian GPT-3 model (trained by [sberbank-ai team](https://github.com/sberbank-ai/ru-gpts)) 
into a web interface where you can conversate with it. All messages stored into db so once signed-in, you will see all your previous messages.

**waring** due to model size, first respond may take a very long time. This is due to the need to download 1.7gb sized model.

### Known issues

* If you experience error below, try specifying nvidia container runtime as described [here](https://github.com/docker/compose/issues/6691#issuecomment-515741713) and set it as the default.

```
Found no NVIDIA driver on your system. Please check that you
have an NVIDIA GPU and installed a driver from ...
```
