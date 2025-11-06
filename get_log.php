<?php
// get_log.php - 增量读取日志，供前端实时显示
$log_file = __DIR__ . "/visit.log";

if (!file_exists($log_file)) {
    echo json_encode(['log' => '', 'offset' => 0]);
    exit;
}

// 增量读取：仅返回上次之后的新增日志
$offset = $_GET['offset'] ?? 0;
$file_size = filesize($log_file);

if ($offset > $file_size) {
    echo json_encode(['log' => '', 'offset' => $file_size]);
    exit;
}

// 读取新增内容并返回
$log_content = file_get_contents($log_file, false, null, $offset);
echo json_encode([
    'log' => $log_content,
    'offset' => $file_size
]);
?>