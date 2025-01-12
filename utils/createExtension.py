import os
import string


def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http',
                                plugin_path=None):
    if plugin_path is None:
        plugin_path = r'./{}/{}_{}_{}_{}'.format("proxy_plugin",proxy_host, proxy_port,proxy_username,proxy_password)


        manifest_json = """
        {
            "version": "1.0.0",
            "name": "Chrome Proxy",
            "manifest_version": 2,
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: ${port}
                },
                bypassList: ["127.0.0.1"]
                }
            };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )
        try:
            os.mkdir(plugin_path)
            manifest_path = os.path.join(plugin_path, 'manifest.json')
            with open(manifest_path, 'w') as f:
                f.write(manifest_json) 

            background_path = os.path.join(plugin_path,'background.js')
            with open(background_path, 'w') as f:
                f.write(background_js)
        except Exception as e:
            pass
            
    return plugin_path