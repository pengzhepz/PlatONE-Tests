# PlatONE-Tests
platone联盟链分层自动化测试代码


## Usage
1. 修改setting.py中的设置项
2. 执行 'pytest' 即可


## Frame
1. cases: 基于pytest框架的测试用例
2. common: 公共方法
3. files: 测试使用的临时文件
4. lib: 
   - chain: 支持底层测试用例的lib
   - env: 用于部署底层链的lib
   - mgr: 联盟链管理后台的page objects
    

## Plan
1. 在lib/env中增加host、node的抽象支持
2. 在lib/chain中增加genesis的抽象支持
3. 支持交易并行