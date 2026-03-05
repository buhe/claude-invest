#!/bin/bash
# 投资分析协调脚本
# 执行5轮分析，每轮6个代理，然后交叉对比并生成最终报告

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查参数
if [ $# -lt 1 ]; then
    log_error "使用方法: $0 <公司名称> [交易所]"
    echo "示例: $0 'Apple Inc.' SEC"
    echo "示例: $0 '腾讯控股' HKEX"
    exit 1
fi

COMPANY_NAME="$1"
EXCHANGE="${2:-SEC}"
INPUT_DIR="input"
ROUND_COUNT=5

log_info "=========================================="
log_info "自动化投资分析系统"
log_info "=========================================="
log_info "公司: $COMPANY_NAME"
log_info "交易所: $EXCHANGE"
log_info "分析轮次: $ROUND_COUNT"
log_info "每轮代理数: 6"
log_info "=========================================="

# 创建输入目录
mkdir -p "$INPUT_DIR"

# 步骤1：准备财报数据
log_info ""
log_info "=== 步骤1: 准备财报数据 ==="
log_info "使用 Claude Code 的 prepare-agent..."

# 这里需要在Claude Code中手动执行
log_warning "请在 Claude Code 中执行以下命令："
log_warning ""
echo "  cd $INPUT_DIR"
echo "  /prepare-agent"
echo "  选择交易所: $EXCHANGE"
echo "  公司名称: $COMPANY_NAME"
log_warning ""
log_warning "等待财报下载完成和 references.md 准备好后，按回车继续..."
read -r

# 检查必要文件
if [ ! -f "$INPUT_DIR/references.md" ]; then
    log_error "references.md 不存在，请先准备财报数据"
    exit 1
fi

# 检查年报文件
REPORT_COUNT=$(find "$INPUT_DIR" -name "*.pdf" -o -name "*.htm" | wc -l)
if [ "$REPORT_COUNT" -lt 3 ]; then
    log_warning "年报文件较少（找到 $REPORT_COUNT 个），建议至少3-5年年报"
    log_warning "是否继续？(y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        log_info "已取消"
        exit 0
    fi
fi

log_success "财报数据准备完成"

# 步骤2：执行5轮分析
log_info ""
log_info "=== 步骤2: 执行 $ROUND_COUNT 轮分析 ==="

for ROUND in $(seq 1 $ROUND_COUNT); do
    log_info ""
    log_info "--- 第 $ROUND 轮分析 ---"
    log_info "启动6个分析代理..."

    # 这里需要在Claude Code中执行
    log_warning "请在 Claude Code 中执行 invest-report skill"
    log_warning "等待第 $ROUND 轮分析完成后，按回车继续..."
    read -r

    # 检查本轮报告
    ROUND_REPORTS=$(find "$INPUT_DIR" -name "*第${ROUND}轮*.md" | wc -l)
    if [ "$ROUND_REPORTS" -lt 6 ]; then
        log_warning "第 $ROUND 轮报告不完整（找到 $ROUND_REPORTS 个，需要6个）"
    else
        log_success "第 $ROUND 轮分析完成（6个报告）"
    fi
done

log_success "所有 $ROUND_COUNT 轮分析完成"

# 步骤3：交叉对比
log_info ""
log_info "=== 步骤3: 交叉对比分析 ==="

MODULES=(
    "业务构成与成本结构"
    "资产负债表"
    "企业估值"
    "资本配置"
    "投资入股与并购"
    "MD&A管理层讨论"
)

for MODULE in "${MODULES[@]}"; do
    log_info "对比 $MODULE 模块..."

    # 这里需要在Claude Code中执行
    log_warning "请在 Claude Code 中使用 diff-agent 对比 $MODULE 的5轮报告"
    log_warning "完成后按回车继续..."
    read -r
done

log_success "交叉对比完成"

# 步骤4：生成最终报告
log_info ""
log_info "=== 步骤4: 生成最终投资研究报告 ==="

log_warning "请在 Claude Code 中使用 invest-report skill 生成最终报告"
log_warning "完成后按回车继续..."
read -r

# 查找最终报告
FINAL_REPORT=$(find "$INPUT_DIR" -name "*投资研究报告.md" -type f | head -n 1)
if [ -z "$FINAL_REPORT" ]; then
    log_error "未找到最终投资研究报告"
    exit 1
fi

log_success "最终报告已生成: $FINAL_REPORT"

# 步骤5：翻译成英文
log_info ""
log_info "=== 步骤5: 翻译成英文 ==="

python3 update_readme.py "$FINAL_REPORT"
if [ $? -eq 0 ]; then
    log_success "英文报告已生成"
else
    log_warning "翻译失败，跳过"
fi

# 步骤6：更新README
log_info ""
log_info "=== 步骤6: 更新 README ==="

if [ -f "README.md" ]; then
    log_success "README 已更新"
else
    log_warning "README.md 不存在，跳过更新"
fi

# 完成
log_info ""
log_info "=========================================="
log_success "分析完成！"
log_info "=========================================="
log_info "报告位置: $FINAL_REPORT"
log_info "README: README.md"
log_info ""
log_info "下一步："
log_info "1. 查看最终报告: cat $FINAL_REPORT"
log_info "2. 查看README: cat README.md"
log_info "3. 提交到Git: git add . && git commit -m 'Add $COMPANY_NAME investment report'"
log_info ""
