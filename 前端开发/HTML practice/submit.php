<?php
// 防止中文乱码
header('Content-Type: text/html; charset=utf-8');

echo "<h2>后台接收的表单数据：</h2>";
echo "<hr>";

// 1. 接收普通文本数据（用户名、密码、电话、日期）
echo "<h3>普通数据：</h3>";
// 检查是否有数据提交
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 用户名
    $username = isset($_POST['username']) ? $_POST['username'] : '未填写';
    echo "用户名：{$username} <br>";
    
    // 密码
    $pwd = isset($_POST['pwd']) ? $_POST['pwd'] : '未填写';
    echo "密码：{$pwd} <br>";
    
    // 电话号码
    $phone = isset($_POST['phone']) ? $_POST['phone'] : '未填写';
    echo "电话号码：{$phone} <br>";
    
    // 选择的日期
    $select_date = isset($_POST['select_date']) ? $_POST['select_date'] : '未选择';
    echo "选择的日期：{$select_date} <br>";

    // 2. 接收上传的文件（图片）
    echo "<h3>上传的文件信息：</h3>";
    if (isset($_FILES['avatar']) && $_FILES['avatar']['error'] === 0) {
        // 文件基本信息
        $file_name = $_FILES['avatar']['name']; // 文件名
        $file_size = $_FILES['avatar']['size']; // 文件大小（字节）
        $file_type = $_FILES['avatar']['type']; // 文件类型
        $tmp_name = $_FILES['avatar']['tmp_name']; // 服务器临时存储路径

        echo "文件名：{$file_name} <br>";
        echo "文件大小：" . round($file_size / 1024, 2) . " KB <br>";
        echo "文件类型：{$file_type} <br>";
        echo "临时路径：{$tmp_name} <br>";

        // 可选：将上传的图片保存到服务器（指定目录）
        $save_path = 'uploads/'; // 新建一个uploads文件夹（和submit.php同目录）
        // 检查文件夹是否存在，不存在则创建
        if (!file_exists($save_path)) {
            mkdir($save_path, 0777, true);
        }
        // 生成唯一文件名（避免覆盖）
        $new_file_name = $save_path . time() . '_' . $file_name;
        // 移动临时文件到指定目录
        if (move_uploaded_file($tmp_name, $new_file_name)) {
            echo "文件上传成功！保存路径：{$new_file_name} <br>";
        } else {
            echo "文件保存失败！<br>";
        }
    } else {
        // 文件上传失败/未上传
        $error_code = $_FILES['avatar']['error'] ?? '无文件上传';
        echo "文件状态：{$error_code}（0=成功，其他=失败）<br>";
    }
} else {
    echo "暂无表单数据提交！<br>";
}

// 返回表单页面的链接
echo "<hr>";
echo '<a href="javascript:history.back()">返回表单页面</a>';
?>