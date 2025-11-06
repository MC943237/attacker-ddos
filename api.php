<?php
// api.php - 接收前端请求，启动/停止Python访问脚本
$action = $_GET['action'] ?? '';
$log_file = __DIR__ . "/visit.log";

// 确保日志文件可写
if (!file_exists($log_file)) {
    touch($log_file);
    chmod($log_file, 0664);
}

// 启动访问（接收前端提交的目标和间隔）
if ($action == 'start') {
    $target = $_POST['target'] ?? '';
    $interval = $_POST['interval'] ?? 1;

    if (empty($target)) {
        echo "错误：目标地址不能为空";
        exit;
    }

    // 停止已有Python进程（避免重复启动）
    exec("pkill -f 'python3 visitor.py'", $output, $return_var);

    // 启动Python脚本（后台运行，接收目标和间隔参数）
    $python_cmd = sprintf(
        "python3 %s/visitor.py '%s' %d >> %s 2>&1 &",
        __DIR__,
        escapeshellarg($target),
        (int)$interval,
        escapeshellarg($log_file)
    );
    exec($python_cmd, $output, $return_var);

    if ($return_var === 0) {
        echo "成功启动：正在无限访问 {$target}（间隔{$interval}秒）";
    } else {
        echo "启动失败：请检查Python环境或目标地址";
    }
}

// 停止访问（终止Python进程）
elseif ($action == 'stop') {
    exec("pkill -f 'python3 visitor.py'", $output, $return_var);
    if ($return_var === 0) {
        echo "已停止所有访问进程";
    } else {
        echo "无运行中的访问进程";
    }
}

else {
    echo "错误：未知操作";
}
?>