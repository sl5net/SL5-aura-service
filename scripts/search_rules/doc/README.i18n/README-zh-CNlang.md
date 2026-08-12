# 所需的逻辑

# Alt+F 和 Alt+G

## **逻辑**

根据描述以及与 **Alt+F** 的类比，**Alt+G** 的逻辑应该如下所示：

### **1。从全文切换 → DITTO (`Alt+G`)**

- **行动**：
- 当前搜索查询（`CURRENT_QUERY`）保存到`SAVED_QUERY`。
- 搜索字段**已清除**。
- `DITTO_STATE` 设置为 `"1"`。
- GUI重新加载

### **2。在 DITTO 模式下**

- **在任何输入（击键）上**：
- DITTO 模式**自动退出** (`DITTO_STATE="0"`)。
- GUI重新加载
- 搜索字段保持**空**（不恢复“SAVED_QUERY”）。

### **3。从 DITTO → 全文切换（再次“Alt+G”）**

- **行动**：
- `DITTO_STATE` 设置为 `"0"`。
- GUI重新加载
- `SAVED_QUERY` 已**恢复**。


---


### **Alt+F 逻辑**

- **从全文→1/文件模式切换**：