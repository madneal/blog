---
title: "如何将网络流转化为内存流 C#"
author: Neal
summary: "本文围绕《如何将网络流转化为内存流 C#》梳理winform开发和后端相关的背景、方法和实践细节，可作为排查与学习记录。"
description: "//将获取的文件流转化为内存流
        public static MemoryStream ConvertStreamToMemoryStream(Stream stream)
        {
            MemoryStream memoryStream = new MemoryStream();
            if (stream != null)"
tags: [后端]
categories: [winform开发]
date: "2015-04-28 11:45:14"
---

```
        //将获取的文件流转化为内存流
        public static MemoryStream ConvertStreamToMemoryStream(Stream stream)
        {
            MemoryStream memoryStream = new MemoryStream();
            if (stream != null)
            {
                byte[] buffer = ReadFull(stream);
                if (buffer != null)
                {
                    var binaryWriter = new BinaryWriter(memoryStream);
                    binaryWriter.Write(buffer);
                }
            }
            return memoryStream;
        }

        public static byte[] ReadFull(Stream input)
        {
            byte[] buffer = new byte[16 * 1024];
            using (MemoryStream ms = new MemoryStream())
            {
                int read;
                while ((read = input.Read(buffer, 0, buffer.Length)) > 0)
                {
                    ms.Write(buffer, 0, read);
                }
                return ms.ToArray();
            }
        }
```
