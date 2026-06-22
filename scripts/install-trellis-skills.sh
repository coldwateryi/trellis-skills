#!/usr/bin/env bash

if [ -n "${BASH_VERSION:-}" ]; then
  if shopt -oq posix 2>/dev/null; then
    printf '%s\n' 'ERROR: install-trellis-skills.sh was started in POSIX sh mode.' >&2
    printf '%s\n' 'This installer supports bash and zsh only. Run with one of:' >&2
    printf '%s\n' '  curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | bash' >&2
    printf '%s\n' '  curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | zsh' >&2
    exit 1
  fi
elif [ -n "${ZSH_VERSION:-}" ]; then
  :
else
  printf '%s\n' 'ERROR: install-trellis-skills.sh only supports bash and zsh.' >&2
  printf '%s\n' 'Run with one of:' >&2
  printf '%s\n' '  curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | bash' >&2
  printf '%s\n' '  curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | zsh' >&2
  exit 1
fi

set -eu

REPO_URL="${TRELLIS_SKILLS_REPO_URL:-https://github.com/coldwateryi/trellis-skills}"
BRANCH="${TRELLIS_SKILLS_BRANCH:-main}"
AGENT_TARGETS="${TRELLIS_SKILLS_AGENT_TARGETS:-both}"

log_timestamp() {
  date '+%Y-%m-%d %H:%M:%S' 2>/dev/null || printf '%s' 'unknown-time'
}

log_message() {
  level="$1"
  shift
  printf '[trellis-skills][%s][%s] %s\n' "$(log_timestamp)" "$level" "$*" >&2
}

log() {
  log_message INFO "$@"
}

warn() {
  log_message WARN "$@"
}

die() {
  log_message ERROR "$@"
  exit 1
}

shell_summary() {
  if [ -n "${BASH_VERSION:-}" ]; then
    printf 'bash %s' "$BASH_VERSION"
  elif [ -n "${ZSH_VERSION:-}" ]; then
    printf 'zsh %s' "$ZSH_VERSION"
  else
    printf 'unknown'
  fi
}

read_line() {
  if [ -r /dev/tty ]; then
    if IFS= read -r "$1" 2>/dev/null </dev/tty; then
      return 0
    fi
  fi

  IFS= read -r "$1"
}

resolve_dir() {
  [ -d "$1" ] || return 1
  (cd "$1" && pwd -P)
}

is_trellis_skills_source() {
  [ -d "$1/scripts" ] &&
    [ -d "$1/trellis-zero-to-mvp" ] &&
    [ -d "$1/trellis-zero-to-mvp-zh" ] &&
    [ -d "$1/trellis-mvp-to-delivery" ] &&
    [ -d "$1/trellis-mvp-to-delivery-zh" ] &&
    [ -d "$1/trellis-implement-tdd" ] &&
    [ -d "$1/trellis-debug-systematic" ] &&
    [ -d "$1/trellis-review-twostage" ] &&
    [ -d "$1/trellis-delivery-controller" ] &&
    [ -d "$1/trellis-skill-assimilator" ] &&
    [ -d "$1/trellis-implement-tdd-zh" ] &&
    [ -d "$1/trellis-debug-systematic-zh" ] &&
    [ -d "$1/trellis-review-twostage-zh" ] &&
    [ -d "$1/trellis-delivery-controller-zh" ] &&
    [ -d "$1/trellis-skill-assimilator-zh" ]
}

detect_local_source_dir() {
  current_dir="$(pwd -P)"

  if [ "${current_dir##*/}" = "scripts" ]; then
    parent_dir="$(resolve_dir "$current_dir/.." 2>/dev/null || true)"
    if [ -n "$parent_dir" ] && is_trellis_skills_source "$parent_dir"; then
      printf '%s\n' "$parent_dir"
      return 0
    fi
  fi

  case "$0" in
    */*)
      script_parent="$(dirname "$0")"
      script_dir="$(resolve_dir "$script_parent" 2>/dev/null || true)"
      if [ -n "$script_dir" ] && [ "${script_dir##*/}" = "scripts" ]; then
        parent_dir="$(resolve_dir "$script_dir/.." 2>/dev/null || true)"
        if [ -n "$parent_dir" ] && is_trellis_skills_source "$parent_dir"; then
          printf '%s\n' "$parent_dir"
          return 0
        fi
      fi
      ;;
  esac

  return 1
}

update_local_source_dir() {
  source_dir="$1"

  [ -d "$source_dir/.git" ] || {
    warn "当前 trellis-skills 目录不是 git checkout，跳过本地源码更新。source_dir=$source_dir"
    return 0
  }

  command -v git >/dev/null 2>&1 || die '需要 git 更新当前 trellis-skills 目录。'

  log "检测到本地 trellis-skills 源码目录: $source_dir"
  log "从 $REPO_URL 更新 $BRANCH 分支到当前 trellis-skills 目录..."

  log "执行 git fetch。repo=$REPO_URL branch=$BRANCH source_dir=$source_dir"
  git -C "$source_dir" fetch "$REPO_URL" "$BRANCH"

  current_branch="$(git -C "$source_dir" rev-parse --abbrev-ref HEAD)"
  log "当前本地源码分支: $current_branch"
  if [ "$current_branch" != "$BRANCH" ]; then
    log "切换本地源码分支。from=$current_branch to=$BRANCH"
    git -C "$source_dir" checkout "$BRANCH"
  fi

  log "执行 fast-forward 合并。source_dir=$source_dir"
  git -C "$source_dir" merge --ff-only FETCH_HEAD
  log "本地 trellis-skills 源码已更新。"
}

is_trellis_project() {
  [ -d "$1/.trellis" ]
}

codex_global_skills_root() {
  if [ -n "${CODEX_HOME:-}" ]; then
    printf '%s/skills\n' "$CODEX_HOME"
    return 0
  fi

  [ -n "${HOME:-}" ] || die '无法确定全局 Codex skill 目录：请设置 CODEX_HOME 或 HOME。'
  printf '%s/.codex/skills\n' "$HOME"
}

claude_global_skills_root() {
  [ -n "${HOME:-}" ] || die '无法确定全局 Claude Code skill 目录：请设置 HOME。'
  printf '%s/.claude/skills\n' "$HOME"
}

normalize_agent_targets() {
  case "$1" in
    ''|both|Both|BOTH|all|All|ALL)
      printf '%s\n' both
      ;;
    codex|Codex|CODEX|agents|Agents|AGENTS)
      printf '%s\n' codex
      ;;
    claude|Claude|CLAUDE|claude-code|Claude-Code|CLAUDE-CODE|claude_code|Claude_Code|CLAUDE_CODE)
      printf '%s\n' claude
      ;;
    *)
      die "未知 Agent 安装目标: $1。请设置 TRELLIS_SKILLS_AGENT_TARGETS=both|codex|claude"
      ;;
  esac
}

prompt_trellis_project_dir() {
  while :; do
    printf '请输入已完成 Trellis 初始化的项目目录: ' >&2
    read_line input_dir || die '未能从终端读取项目目录。请在交互式终端中运行安装命令。'

    [ -n "$input_dir" ] || {
      warn '目录不能为空。'
      continue
    }

    resolved_dir="$(resolve_dir "$input_dir" 2>/dev/null || true)"
    [ -n "$resolved_dir" ] || {
      warn "目录不存在: $input_dir"
      continue
    }

    if is_trellis_project "$resolved_dir"; then
      log "已选择 Trellis 项目目录: $resolved_dir"
      printf 'project|%s\n' "$resolved_dir"
      return 0
    fi

    warn "该目录未发现 .trellis/。path=$resolved_dir"
    if choose_global_install "$resolved_dir"; then
      log "用户选择安装到全局 skill 目录。"
      printf 'global|\n'
      return 0
    fi

    warn '请先运行 trellis init，或输入其他已初始化 Trellis 的项目目录。'
  done
}

choose_global_install() {
  checked_dir="$1"

  while :; do
    printf '目录 %s 不是 Trellis 项目。是否改为安装到全局 skill 目录? [y/N]: ' "$checked_dir" >&2
    read_line answer || die '未能从终端读取全局安装选择。请在交互式终端中运行安装命令。'

    case "$answer" in
      Y|y|Yes|yes|YES|是)
        return 0
        ;;
      ''|N|n|No|no|NO|否)
        return 1
        ;;
      *)
        warn '请输入 y/yes/是 或 n/no/否。'
        ;;
    esac
  done
}

choose_language() {
  target_dir="$1"

  while :; do
    printf '是否安装中文版 skill 到 %s ? [Y/n]: ' "$target_dir" >&2
    read_line answer || die '未能从终端读取语言选择。请在交互式终端中运行安装命令。'

    case "$answer" in
      ''|Y|y|Yes|yes|YES|是)
        log "语言选择: zh，安装中文版 skills。"
        printf '%s\n' zh
        return 0
        ;;
      N|n|No|no|NO|否)
        log "语言选择: en，安装英文版 skills。"
        printf '%s\n' en
        return 0
        ;;
      *)
        warn '请输入 y/yes/是 或 n/no/否。'
        ;;
    esac
  done
}

download_archive() {
  archive_url="$REPO_URL/archive/refs/heads/$BRANCH.tar.gz"
  archive_path="$1"
  log "准备下载源码压缩包。url=$archive_url output=$archive_path"

  if command -v curl >/dev/null 2>&1; then
    log '使用 curl 下载源码压缩包。'
    curl -fsSL "$archive_url" -o "$archive_path"
  elif command -v wget >/dev/null 2>&1; then
    log '使用 wget 下载源码压缩包。'
    wget -qO "$archive_path" "$archive_url"
  else
    die '需要 curl 或 wget 下载 GitHub main 分支压缩包。'
  fi

  log "源码压缩包下载完成。path=$archive_path"
}

copy_skills_to_install_root() {
  source_dir="$1"
  install_root="$2"
  shift 2
  skills=("$@")

  log "准备安装 skills。source_dir=$source_dir install_root=$install_root skills=\"${skills[*]}\""
  mkdir -p "$install_root"
  log "已确保安装目录存在: $install_root"

  for skill in "${skills[@]}"; do
    source_skill="$source_dir/$skill"
    target_skill="$install_root/$skill"
    log "开始安装 skill。skill=$skill source=$source_skill target=$target_skill"

    [ -d "$source_skill" ] || die "GitHub 源目录缺少 skill: $skill"

    if [ -d "$target_skill" ]; then
      log "目标 skill 已存在，将先删除旧目录: $target_skill"
    fi
    rm -rf "$target_skill"
    cp -R "$source_skill" "$install_root/"
    log "已安装: $target_skill"
  done

  log "完成。安装目录: $install_root"
}

install_skills() {
  install_scope="$1"
  target_dir="$2"
  language="$3"
  local_source_dir="${4:-}"
  agent_targets="$(normalize_agent_targets "$AGENT_TARGETS")"

  case "$language" in
    zh)
      skills=(
        'trellis-zero-to-mvp-zh'
        'trellis-mvp-to-delivery-zh'
        'trellis-implement-tdd-zh'
        'trellis-debug-systematic-zh'
        'trellis-review-twostage-zh'
        'trellis-delivery-controller-zh'
        'trellis-skill-assimilator-zh'
      )
      ;;
    en)
      skills=(
        'trellis-zero-to-mvp'
        'trellis-mvp-to-delivery'
        'trellis-implement-tdd'
        'trellis-debug-systematic'
        'trellis-review-twostage'
        'trellis-delivery-controller'
        'trellis-skill-assimilator'
      )
      ;;
    *)
      die "未知语言选项: $language"
      ;;
  esac

  log "准备安装 skills。install_scope=$install_scope target_dir=$target_dir language=$language agent_targets=$agent_targets skills=\"${skills[*]}\""

  tmp_dir=''

  cleanup() {
    if [ -n "$tmp_dir" ]; then
      log "清理临时目录: $tmp_dir"
      rm -rf "$tmp_dir"
    fi
  }
  trap cleanup EXIT INT TERM

  if [ -n "$local_source_dir" ]; then
    source_dir="$local_source_dir"
    log "使用已更新的本地 trellis-skills 源码安装 skill。"
  else
    tmp_dir="$(mktemp -d 2>/dev/null || mktemp -d -t trellis-skills)"
    archive_path="$tmp_dir/trellis-skills.tar.gz"
    log "已创建临时目录: $tmp_dir"

    log "从 $REPO_URL 下载 $BRANCH 分支..."
    download_archive "$archive_path"

    log "解压源码压缩包到临时目录。archive=$archive_path tmp_dir=$tmp_dir"
    tar -xzf "$archive_path" -C "$tmp_dir"
    source_dir="$(find "$tmp_dir" -maxdepth 1 -type d -name 'trellis-skills-*' | head -n 1)"
    [ -n "$source_dir" ] || die '解压后未找到 trellis-skills 源目录。'
    log "已定位解压后的源码目录: $source_dir"
  fi

  case "$install_scope" in
    project)
      if [ "$agent_targets" = "both" ] || [ "$agent_targets" = "codex" ]; then
        copy_skills_to_install_root "$source_dir" "$target_dir/.agents/skills" "${skills[@]}"
      fi

      if [ "$agent_targets" = "both" ] || [ "$agent_targets" = "claude" ]; then
        copy_skills_to_install_root "$source_dir" "$target_dir/.claude/skills" "${skills[@]}"
      fi
      ;;
    global)
      if [ "$agent_targets" = "both" ] || [ "$agent_targets" = "codex" ]; then
        copy_skills_to_install_root "$source_dir" "$(codex_global_skills_root)" "${skills[@]}"
      fi

      if [ "$agent_targets" = "both" ] || [ "$agent_targets" = "claude" ]; then
        copy_skills_to_install_root "$source_dir" "$(claude_global_skills_root)" "${skills[@]}"
      fi
      ;;
    *)
      die "未知安装范围: $install_scope"
      ;;
  esac

  log "完成。安装目标: $agent_targets"
}

main() {
  current_dir="$(pwd -P)"
  log "启动安装脚本。shell=$(shell_summary) pid=$$ cwd=$current_dir"
  normalized_agent_targets="$(normalize_agent_targets "$AGENT_TARGETS")"
  log "安装源配置。repo=$REPO_URL branch=$BRANCH agent_targets=$normalized_agent_targets"

  local_source_dir="$(detect_local_source_dir 2>/dev/null || true)"
  if [ -n "$local_source_dir" ]; then
    log "检测到可用的本地 trellis-skills 源码目录: $local_source_dir"
  else
    log "未检测到本地 trellis-skills 源码目录，将按需下载远程源码。"
  fi

  if [ -n "$local_source_dir" ]; then
    update_local_source_dir "$local_source_dir"
  fi

  if is_trellis_project "$current_dir"; then
    install_scope='project'
    target_dir="$current_dir"
    log "当前目录是 Trellis 项目，使用当前目录作为安装目标: $target_dir"
  else
    warn "当前目录未发现 .trellis/，不是已初始化的 Trellis 项目。cwd=$current_dir"
    target_spec="$(prompt_trellis_project_dir)"
    install_scope="${target_spec%%|*}"
    target_dir="${target_spec#*|}"
  fi

  if [ "$install_scope" = "global" ]; then
    target_label='全局 skill 目录'
  else
    target_label="$target_dir"
  fi

  language="$(choose_language "$target_label")"
  log "进入安装阶段。install_scope=$install_scope target_dir=$target_dir language=$language"
  install_skills "$install_scope" "$target_dir" "$language" "$local_source_dir"
}

main "$@"
