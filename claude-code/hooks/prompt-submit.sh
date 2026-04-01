#!/bin/bash
# Claude PRISM — Unified UserPromptSubmit Hook v2.0
# Merged: prompt-guard.sh + auto-skill-router.sh
# Fires before each user prompt reaches Claude.
# 1. Detects confidential topics → injects privacy reminder
# 2. Pattern-matches prompt to skills → injects loading directives

# Skip during ralph-loop
if [ -f "$HOME/.claude/ralph-loop.local.md" ] || \
   [ -f "$HOME/.claude/plugins/ralph-loop/ralph-loop.local.md" ] || \
   [ -n "$RALPH_LOOP_ACTIVE" ]; then
    exit 0
fi

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

if ! command -v jq &>/dev/null; then
    exit 0
fi

PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)
[ -z "$PROMPT" ] && exit 0

P=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# ============================================================
# PART 1: Confidentiality Guard
# ============================================================
CONFIDENTIAL=false

if echo "$P" | grep -qE '(condescend|frustrat|upset|angry|unfair|power dynamic|hypocrit).*(partner|mentor|cofounder|co-founder)'; then
    CONFIDENTIAL=true
fi
if echo "$P" | grep -qE '(equity split|compensation|revenue share|overpaid|underpaid|give.*(all|back).*revenue)'; then
    CONFIDENTIAL=true
fi
if echo "$P" | grep -qE '(separate.*business|new llc|on my own|dont tell|keep.*secret|between us)'; then
    CONFIDENTIAL=true
fi
if echo "$P" | grep -qE '(confidential|off the record|private|dont share|don.t share)'; then
    CONFIDENTIAL=true
fi
if echo "$P" | grep -qE '(bad mentor|good mentor|what do you think.*(partner|mentor|cofounder))'; then
    CONFIDENTIAL=true
fi

if [ "$CONFIDENTIAL" = true ]; then
    echo "[PRISM CONFIDENTIALITY NOTICE: This conversation contains sensitive personal/strategic content. Do NOT extract relationship dynamics, personal assessments, or strategic positioning into SOPs, memory bank, or any shared files. Action items and process improvements may be extracted only if stripped of interpersonal context.]"
fi

# ============================================================
# PART 2: Auto Skill Router
# ============================================================
SKILLS=""

# SEO / KP Sprint
echo "$P" | grep -qE '(schema|json-ld|structured data|markup)' && SKILLS="${SKILLS}Load /schema-markup skill. "
echo "$P" | grep -qE '(seo audit|site audit|technical seo|crawl|core web vitals)' && SKILLS="${SKILLS}Load /seo-audit skill. "
echo "$P" | grep -qE '(geo |aeo|ai overview|ai search|citab|perplexity|chatgpt citation)' && SKILLS="${SKILLS}Load /geo-optimizer skill. "
echo "$P" | grep -qE '(entity|kgmid|knowledge graph|knowledge panel|kp sprint)' && SKILLS="${SKILLS}Load /entity-builder skill. "
echo "$P" | grep -qE '(keyword|backlink|ahrefs|domain authority|content gap)' && SKILLS="${SKILLS}Load /keyword-research skill. "
echo "$P" | grep -qE '(search console|gsc|ranking|ctr|impressions|indexing)' && SKILLS="${SKILLS}Load /gsc-insights skill. "
echo "$P" | grep -qE '(competitor|competitive|rival|compare.*site|market position)' && SKILLS="${SKILLS}Load /competitor-intel skill. "

# Content Production
echo "$P" | grep -qE '(article qa|quality gate|18.step|proofread|check.*article)' && SKILLS="${SKILLS}Load /article-quality-gate skill. "
echo "$P" | grep -qE '(batch.*article|write.*[0-9]+.*article|parallel.*content|mass produc)' && SKILLS="${SKILLS}Load /batch-content skill. "
echo "$P" | grep -qE '(transcript|youtube.*article|whisper|video.*to.*article|podcast.*to)' && SKILLS="${SKILLS}Load /transcript-pipeline skill. "
echo "$P" | grep -qE '(content calendar|editorial|monthly.*plan|quarterly.*content|topic wheel.*plan)' && SKILLS="${SKILLS}Load /content-calendar skill. "
echo "$P" | grep -qE '(social media|linkedin.*post|facebook.*post|instagram|tweet|social.*content)' && SKILLS="${SKILLS}Load /social-content skill. "
echo "$P" | grep -qE '(wordpress|wp.*publish|rankmath|meta.*description|publish.*article)' && SKILLS="${SKILLS}Load /wp-publisher skill. "
echo "$P" | grep -qE '(meta.article|document.*what.*did|how we built|process article|write.*meta)' && SKILLS="${SKILLS}Load /meta-article skill. "
echo "$P" | grep -qE '(definitive article|canonical article|pillar content|hub article|consolidate.*article)' && SKILLS="${SKILLS}Load /definitive-article skill. "

# Business Operations
echo "$P" | grep -qE '(basecamp|to.do|project update|post.*update.*basecamp)' && SKILLS="${SKILLS}Load /basecamp-ops skill. "
echo "$P" | grep -qE '(inbox|email.*triage|check.*email|unread|what.*needs.*attention)' && SKILLS="${SKILLS}Load /inbox-triage skill. "
echo "$P" | grep -qE '(meeting.*note|action.*item|call.*summary|zoom.*transcript|meeting.*transcript)' && SKILLS="${SKILLS}Load /meeting-capture skill. "
echo "$P" | grep -qE '(client.*report|maa.*report|monthly.*review|kp.*progress|weekly.*report.*client)' && SKILLS="${SKILLS}Load /client-report skill. "
echo "$P" | grep -qE '(outreach|cold.*email|prospect.*sequence|follow.*up.*email|nurture)' && SKILLS="${SKILLS}Load /outreach-sequence skill. "
echo "$P" | grep -qE '(client.*status|client.*snapshot|what.*happening.*with|how.*is.*client)' && SKILLS="${SKILLS}Load /client-snapshot skill. "
echo "$P" | grep -qE '(content.*pipeline|production.*status|what.*in.*pipeline|content.*status)' && SKILLS="${SKILLS}Load /content-pipeline-status skill. "

# PRISM-only skills (not auto-discovered)
echo "$P" | grep -qE '(write.*article|article.*from.*transcript|batch.*write)' && SKILLS="${SKILLS}Load article-writer from ~/Documents/Claude/PRISM/skills/article-writer.md. "
echo "$P" | grep -qE '(content factory|6.*stage|plumbing.*produce|produce.*process)' && SKILLS="${SKILLS}Load content-factory from ~/Documents/Claude/PRISM/skills/content-factory.md. "
echo "$P" | grep -qE '(dollar.*day|\$1.*day|boost.*content|paid.*social|promote.*stage)' && SKILLS="${SKILLS}Load dollar-a-day from ~/Documents/Claude/PRISM/skills/dollar-a-day.md. "
echo "$P" | grep -qE '(influence.*report|authority.*score|quick.*audit|presence.*audit)' && SKILLS="${SKILLS}Load influence-report-card from ~/Documents/Claude/PRISM/skills/influence-report-card.md. "
echo "$P" | grep -qE '(repurpos|long.*form.*to.*short|multi.*platform|turn.*into.*posts)' && SKILLS="${SKILLS}Load content-repurposing from ~/Documents/Claude/PRISM/skills/content-repurposing.md. "
echo "$P" | grep -qE '(personal.*brand.*site|wordpress.*build|kp.*site)' && SKILLS="${SKILLS}Load personal-brand-site from ~/Documents/Claude/PRISM/skills/personal-brand-site.md. "
echo "$P" | grep -qE '(prospect|discovery.*call|qualify.*lead|new.*lead|follow.*up.*prospect)' && SKILLS="${SKILLS}Load prospect-followup from ~/Documents/Claude/PRISM/skills/prospect-followup.md. "

if [ -n "$SKILLS" ]; then
    echo "[PRISM AUTO-ROUTER: ${SKILLS}Follow the skill instructions exactly. Use good-examples from ~/Documents/Claude/PRISM/skills/good-examples/ if available for this content type.]"
fi

exit 0
