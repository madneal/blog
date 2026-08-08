---
title: "ROT13加密和解密"
author: Neal
summary: "本文围绕《ROT13加密和解密》展开，重点梳理问题和代码等内容，提炼背景、思路与实践注意点。"
description: "问题ROT13（回转13位）是一种简易的替换式密码算法。它是一种在英文网络论坛用作隐藏八卦、妙句、谜题解答以及某些脏话的工具，目的是逃过版主或管理员的匆匆一瞥。ROT13 也是过去在古罗马开发的凯撒密码的一种变体。ROT13是它自身的逆反，即：要还原成原文只要使用同一算法即可得，故同样的操作可用于加密与解密。该算法并没有提供真正密码学上的保全，故它不应该被用于需要保全的用途上。它常常被当作弱加密示例"
tags: [算法]
categories: [算法OJ]
date: "2015-04-11 10:16:26"
lastmod: "2026-08-08"
---

## 问题 ##
ROT13（回转13位）是一种简易的替换式密码算法。它是一种在英文网络论坛用作隐藏八卦、妙句、谜题解答以及某些脏话的工具，目的是逃过版主或管理员的匆匆一瞥。ROT13 也是过去在古罗马开发的凯撒密码的一种变体。ROT13是它自身的逆反，即：要还原成原文只要使用同一算法即可得，故同样的操作可用于加密与解密。该算法并没有提供真正密码学上的保全，故它不应该被用于需要保全的用途上。它常常被当作弱加密示例的典型。

应用ROT13到一段文字上仅仅只需要检查字母顺序并取代它在13位之后的对应字母，有需要超过时则重新绕回26英文字母开头即可。A换成N、B换成O、依此类推到M换成Z，然后串行反转：N换成A、O换成B、最后Z换成M（如图所示）。只有这些出现在英文字母里的字符受影响；数字、符号、空白字符以及所有其他字符都不变。替换后的字母大小写保持不变。

 

例如，下面的英文笑话，精华句被ROT13所隐匿：

How can you tell an extrovert from an

introvert at NSA? Va gur ryringbef,

gur rkgebireg ybbxf ng gur BGURE thl'f fubrf.

通过ROT13转换，该笑话的解答揭露如下：

Ubj pna lbh gryy na rkgebireg sebz na

vagebireg ng AFN? In the elevators,

the extrovert looks at the OTHER guy's shoes.

第二次使用ROT13将恢复为原文。

Input 

第1行：一个整数T（1≤T≤10）为问题数。

接下来共T行。每行为长度不超过1000个字符的一段文字。内含大小写字母、空格、数字和各种符号等。

Output 

对于每个问题，输出一行问题的编号（0开始编号，格式：case #0: 等）。

然后对应每个问题在一行中输出经过ROT13加密后的一段文字。

Sample Input 

3

How can you tell an extrovert from an

introvert at NSA? Va gur ryringbef,

gur rkgebireg ybbxf ng gur BGURE thl'f fubrf.

Sample Output 

case #0:

Ubj pna lbh gryy na rkgebireg sebz na

case #1:

vagebireg ng AFN? In the elevators,

case #2:

the extrovert looks at the OTHER guy's shoes.
## 代码 ##

```
#include<stdio.h>
#include<string.h>
char str[1010];
char tmp[1010];
int Encry(char x)
{
	int a,b;
	char tmp;
	b = x;
	a = x + 13;
	if(b >= 97 && b <= 122)
	{	
		if (a > 122)
		{
		a = a - 26;
		}
	}
	else if (b >= 65 && b <= 90)
	{
		if(a > 90)
		{
			a = a- 26;
		}
	}
	else
	{
	a =b;
	}
	return a;
}
int main()
{
	int cas = 0;
	int T;
	int num[1010];
	scanf("%d",&T);
	strcpy(str,"");
	while(T--)
	{
	while(strcmp(str,"")==0)
	gets(str);
	memset(num,0,sizeof(num[0]));
	int len = strlen(str);
	for(int i = 0;i < len;i ++)
	{
		num[i] = Encry(str[i]);
	}
	printf("case #%d:\n",cas++);
	for(int i = 0;i < len;i ++)
	{
		if(i == len - 1)
	{
		printf("%c\n",num[i]);
	}
	else
	{
		printf("%c",num[i]);
	}
	}
	strcpy(str,"");
}
return 0;
}
```


## 算法性质

ROT13 是凯撒密码的特例：字母表旋转 13 位。因 26=13×2，**加密与解密同一操作**。它不提供密码学安全，只适合论坛剧透遮罩等场景。

## 实现注意

- 只处理 A–Z / a–z，数字与符号保持不变  
- 非 ASCII 文本不适用经典 ROT13  
- CTF 里常与 Base64、多重编码叠加  

## 安全课上的位置

用 ROT13 当「加密」是典型错误示例：说明 **混淆 ≠ 加密**。真正保密需要现代 AEAD（如 AES-GCM）与密钥管理。

## 小结

认识 ROT13 是为了识破它，而不是用它保护数据。见「加密」字样先问：算法、密钥、威胁模型分别是什么。


## 快速自测

对字符串 `Hello` 应用 ROT13 应得 `Uryyb`；再应用一次回到 `Hello`。若结果不对，检查是否错误处理了非字母字符。理解对称性有助于在 CTF 里一眼识破。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。


## 译者实践注

本文为技术译文/整理，原文版权归原作者所有。阅读时建议结合自身环境验证命令与结论；若原文年代较早，请以官方最新文档与安全通告为准。欢迎通过 issue 或邮件指出过时之处。
