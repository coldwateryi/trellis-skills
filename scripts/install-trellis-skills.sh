#!/usr/bin/env sh
set -eu

REPO_URL="${TRELLIS_SKILLS_REPO_URL:-https://github.com/coldwateryi/trellis-skills}"
BRANCH="${TRELLIS_SKILLS_BRANCH:-main}"

log() {
  printf '%s\n' "$*" >&2
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
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
    [ -d "$1/trellis-mvp-to-delivery-zh" ]
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
    log "当前 trellis-skills 目录不是 git checkout，跳过本地源码更新。"
    return 0
  }

  command -v git >/dev/null 2>&1 || die '需要 git 更新当前 trellis-skills 目录。'

  log "检测到本地 trellis-skills 源码目录: $source_dir"
  log "从 $REPO_URL 更新 $BRANCH 分支到当前 trellis-skills 目录..."

  git -C "$source_dir" fetch "$REPO_URL" "$BRANCH"

  current_branch="$(git -C "$source_dir" rev-parse --abbrev-ref HEAD)"
  if [ "$current_branch" != "$BRANCH" ]; then
    git -C "$source_dir" checkout "$BRANCH"
  fi

  git -C "$source_dir" merge --ff-only FETCH_HEAD
  log "本地 trellis-skills 源码已更新。"
}

is_trellis_project() {
  [ -d "$1/.trellis" ]
}

prompt_trellis_project_dir() {
  while :; do
    printf '请输入已完成 Trellis 初始化的项目目录: ' >&2
    IFS= read -r input_dir || exit 1

    [ -n "$input_dir" ] || {
      log '目录不能为空。'
      continue
    }

    resolved_dir="$(resolve_dir "$input_dir" 2>/dev/null || true)"
    [ -n "$resolved_dir" ] || {
      log "目录不存在: $input_dir"
      continue
    }

    if is_trellis_project "$resolved_dir"; then
      printf '%s\n' "$resolved_dir"
      return 0
    fi

    log "该目录未发现 .trellis/，请先运行 trellis init 或输入其他项目目录。"
  done
}

choose_language() {
  target_dir="$1"

  while :; do
    printf '是否安装中文版 skill 到 %s ? [Y/n]: ' "$target_dir" >&2
    IFS= read -r answer || exit 1

    case "$answer" in
      ''|Y|y|Yes|yes|YES|是)
        printf '%s\n' zh
        return 0
        ;;
      N|n|No|no|NO|否)
        printf '%s\n' en
        return 0
        ;;
      *)
        log '请输入 y/yes/是 或 n/no/否。'
        ;;
    esac
  done
}

download_archive() {
  archive_url="$REPO_URL/archive/refs/heads/$BRANCH.tar.gz"
  archive_path="$1"

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$archive_url" -o "$archive_path"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$archive_path" "$archive_url"
  else
    die '需要 curl 或 wget 下载 GitHub main 分支压缩包。'
  fi
}

install_skills() {
  target_dir="$1"
  language="$2"
  local_source_dir="${3:-}"

  case "$language" in
    zh)
      skills='trellis-zero-to-mvp-zh trellis-mvp-to-delivery-zh'
      ;;
    en)
      skills='trellis-zero-to-mvp trellis-mvp-to-delivery'
      ;;
    *)
      die "未知语言选项: $language"
      ;;
  esac

  install_root="$target_dir/.agents/skills"
  mkdir -p "$install_root"

  tmp_dir=''

  cleanup() {
    if [ -n "$tmp_dir" ]; then
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

    log "从 $REPO_URL 下载 $BRANCH 分支..."
    download_archive "$archive_path"

    tar -xzf "$archive_path" -C "$tmp_dir"
    source_dir="$(find "$tmp_dir" -maxdepth 1 -type d -name 'trellis-skills-*' | head -n 1)"
    [ -n "$source_dir" ] || die '解压后未找到 trellis-skills 源目录。'
  fi

  for skill in $skills; do
    source_skill="$source_dir/$skill"
    target_skill="$install_root/$skill"

    [ -d "$source_skill" ] || die "GitHub 源目录缺少 skill: $skill"

    rm -rf "$target_skill"
    cp -R "$source_skill" "$install_root/"
    log "已安装: $target_skill"
  done

  log "完成。安装目录: $install_root"
}

main() {
  current_dir="$(pwd -P)"
  local_source_dir="$(detect_local_source_dir 2>/dev/null || true)"

  if [ -n "$local_source_dir" ]; then
    update_local_source_dir "$local_source_dir"
  fi

  if is_trellis_project "$current_dir"; then
    target_dir="$current_dir"
  else
    log "当前目录未发现 .trellis/，不是已初始化的 Trellis 项目。"
    target_dir="$(prompt_trellis_project_dir)"
  fi

  language="$(choose_language "$target_dir")"
  install_skills "$target_dir" "$language" "$local_source_dir"
}

main "$@"
