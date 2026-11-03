# Environment of the HFT Loveland calculation chain. K = work dir (W for the final run, W/dryrun for the dry run)
export S=/tmp/claude-0/-home-user-reading-plans/8286ed83-02db-5490-a21c-6cf4b9d790c9/scratchpad
export W=$S/hf
export T=$S/skill/take-off-metal-frame-drywall/tools
export PDF=$W/plano/bidset_ORIG_SIN_MARKUPS.pdf
export K=${K:-$W}
export BITACORA=$K/bitacora.jsonl
export TAKEOFF_WORK=$K/etapas
