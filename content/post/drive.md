---
title: "Google Drive 的信息检索"
author: Neal
tags: [开发]
keywords: [开发,Google Drive,API]
date: "2023-08-28" 
---

对于使用 Google 全家桶的公司，Google 文档类的信息泄露也时常发生。出现这种情况主要的原因是文档的权限设置问题，用户可能将文档配置为 anyoneCanFind, anyoneWithLink, domainCanFind, domainWithLink，这四种权限都属于比较公开的权限。后两个属于在域内可以查看到文档，一般来说也是不提倡如此设置，尤其是文档中包含敏感信息的。

## Auth

如果要使用 Google Drive 的 API，毫无疑问，Google Workspace 的 Auth 则是第一步。对于 Auth，一般可以通过 OAuth 或者 service account 来进行实现，但是 service account 有一个问题是，默认这个 service acount 并没有赋予这个 servive account 这个域内所有资源的访问权限。必须要将这个文档分享给 service account，它才可以访问。这将会影响到对于 domainCanFind 以及 domainWithLink 的文档的搜索。解决办法是需要 delegate domain-wide authority,相当于是对于这个 service account 进行额外的授权，详细的介绍可以参考这个[文档](https://developers.google.com/cloud-search/docs/guides/delegation)。当然，这个授权需要管理员账号来进行，如果申请比较麻烦的话，还可以通过使用 OAuth 的方式来进行认证，这也是 Google Drive API 文档指引中介绍使用的方式。

通过 OAuth 来使用 Drive API 也需要三个步骤：

1. 启用 API
2. 配置 OAuth 应用
3. 生成 Credentials

详细介绍可以参考谷歌的[文档](https://developers.google.com/drive/api/quickstart/go)介绍，基本上每一步都有详细的介绍。建议可以按照文档的方式来进行操作，OAuth 生成方式会用到一个 credentials.json 文件。如果对 OAuth 流程比较了解的话，应该知道流程中会有一个授权的流程。Go 的官方文档已经提供了一个授权的 demo，通过运行代码可以获取 autorization code，通过 aurhorization code 可以生成 token.json。对于内部应用，生成的 token.json 包含 refresh_token 的话，这个 token 是不会过期的。

```go 
package main

import (
        "context"
        "encoding/json"
        "fmt"
        "log"
        "net/http"
        "os"

        "golang.org/x/oauth2"
        "golang.org/x/oauth2/google"
        "google.golang.org/api/drive/v3"
        "google.golang.org/api/option"
)

// Retrieve a token, saves the token, then returns the generated client.
func getClient(config *oauth2.Config) *http.Client {
        // The file token.json stores the user's access and refresh tokens, and is
        // created automatically when the authorization flow completes for the first
        // time.
        tokFile := "token.json"
        tok, err := tokenFromFile(tokFile)
        if err != nil {
                tok = getTokenFromWeb(config)
                saveToken(tokFile, tok)
        }
        return config.Client(context.Background(), tok)
}

// Request a token from the web, then returns the retrieved token.
func getTokenFromWeb(config *oauth2.Config) *oauth2.Token {
        authURL := config.AuthCodeURL("state-token", oauth2.AccessTypeOffline)
        fmt.Printf("Go to the following link in your browser then type the "+
                "authorization code: \n%v\n", authURL)

        var authCode string
        if _, err := fmt.Scan(&authCode); err != nil {
                log.Fatalf("Unable to read authorization code %v", err)
        }

        tok, err := config.Exchange(context.TODO(), authCode)
        if err != nil {
                log.Fatalf("Unable to retrieve token from web %v", err)
        }
        return tok
}

// Retrieves a token from a local file.
func tokenFromFile(file string) (*oauth2.Token, error) {
        f, err := os.Open(file)
        if err != nil {
                return nil, err
        }
        defer f.Close()
        tok := &oauth2.Token{}
        err = json.NewDecoder(f).Decode(tok)
        return tok, err
}

// Saves a token to a file path.
func saveToken(path string, token *oauth2.Token) {
        fmt.Printf("Saving credential file to: %s\n", path)
        f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0600)
        if err != nil {
                log.Fatalf("Unable to cache oauth token: %v", err)
        }
        defer f.Close()
        json.NewEncoder(f).Encode(token)
}

func main() {
        ctx := context.Background()
        b, err := os.ReadFile("credentials.json")
        if err != nil {
                log.Fatalf("Unable to read client secret file: %v", err)
        }

        // If modifying these scopes, delete your previously saved token.json.
        config, err := google.ConfigFromJSON(b, drive.DriveMetadataReadonlyScope)
        if err != nil {
                log.Fatalf("Unable to parse client secret file to config: %v", err)
        }
        client := getClient(config)

        srv, err := drive.NewService(ctx, option.WithHTTPClient(client))
        if err != nil {
                log.Fatalf("Unable to retrieve Drive client: %v", err)
        }

        r, err := srv.Files.List().PageSize(10).
                Fields("nextPageToken, files(id, name)").Do()
        if err != nil {
                log.Fatalf("Unable to retrieve files: %v", err)
        }
        fmt.Println("Files:")
        if len(r.Files) == 0 {
                fmt.Println("No files found.")
        } else {
                for _, i := range r.Files {
                        fmt.Printf("%s (%s)\n", i.Name, i.Id)
                }
        }
}
```

完整的项目代码可以参考 GitHub 上面的[代码仓库](https://github.com/googleworkspace/go-samples/blob/main/drive/quickstart/quickstart.go)。上面有完整的代码， `go run quickstart.go` 即可运行获取 token 文件。

## 检索

在我们获取 credentials.json 以及 token.json 文件之后，就已经能够完成 API 的鉴权。Files.List API 是进行文件检索的核心 API。完整的搜索语法可以参考 Google 的[文档](https://developers.google.com/drive/api/guides/ref-search-terms)。

![image.png](https://s2.loli.net/2023/09/07/spyaPztHqLovZ69.png)

另外一个重要的实现就是 API 的翻页功能。不过 API 的翻页和其它普通的翻页不太一样，因为它不是使用普通的 page_no 来进行翻页。它是通过 pageToken 来进行翻页，而 pageToken 是随机字符串，而不是普通的数字。

```go
func getResults(keyword, query string) {
	pageToken := ""
	results := make([]file.File, 0)
	for {
		r, err := scanner.service.Files.List().PageSize(10).Fields("nextPageToken,files(*)").
			Q(query).Corpus("domain").
			PageToken(pageToken).Do()
		if err != nil {
			
		}
		results = append(results, r.file())
		if r.NextPageToken == "" {
			break
		}
		pageToken = r.NextPageToken
	}
	return results
}
```

通过 `Fields` 可以指定响应里面返回的字段，通过 Corpus 可以限定域内资源的搜索。至此，基本上可以实现通过关键词实现对 Google Drive 信息的检索。虽然 Google Drive 支持关键词的全文搜索，但是搜索结果不支持展示匹配的上下文，这是唯一一个比较欠缺的地方。