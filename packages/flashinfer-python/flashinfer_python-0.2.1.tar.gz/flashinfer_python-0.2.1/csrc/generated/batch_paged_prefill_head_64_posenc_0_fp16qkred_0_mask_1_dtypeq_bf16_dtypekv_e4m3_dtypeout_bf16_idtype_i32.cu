#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = BatchPrefillPagedParams<nv_bfloat16, __nv_fp8_e4m3, nv_bfloat16, int32_t>;

using AttentionVariant1 = ComposedAttention<ParamsT, get_variant_code(
    false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>;

template cudaError_t BatchPrefillWithPagedKVCacheDispatched<128, 64, PosEncodingMode::kNone, 0, MaskMode::kCausal, AttentionVariant1>(
    ParamsT params,
    nv_bfloat16* tmp_v,
    float* tmp_s, cudaStream_t stream);
    
template cudaError_t BatchPrefillWithPagedKVCacheDispatched<64, 64, PosEncodingMode::kNone, 0, MaskMode::kCausal, AttentionVariant1>(
    ParamsT params,
    nv_bfloat16* tmp_v,
    float* tmp_s, cudaStream_t stream);
    
template cudaError_t BatchPrefillWithPagedKVCacheDispatched<16, 64, PosEncodingMode::kNone, 0, MaskMode::kCausal, AttentionVariant1>(
    ParamsT params,
    nv_bfloat16* tmp_v,
    float* tmp_s, cudaStream_t stream);
    

using AttentionVariant2 = ComposedAttention<ParamsT, get_variant_code(
    false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>;

template cudaError_t BatchPrefillWithPagedKVCacheDispatched<128, 64, PosEncodingMode::kNone, 0, MaskMode::kCausal, AttentionVariant2>(
    ParamsT params,
    nv_bfloat16* tmp_v,
    float* tmp_s, cudaStream_t stream);
    
template cudaError_t BatchPrefillWithPagedKVCacheDispatched<64, 64, PosEncodingMode::kNone, 0, MaskMode::kCausal, AttentionVariant2>(
    ParamsT params,
    nv_bfloat16* tmp_v,
    float* tmp_s, cudaStream_t stream);
    
template cudaError_t BatchPrefillWithPagedKVCacheDispatched<16, 64, PosEncodingMode::kNone, 0, MaskMode::kCausal, AttentionVariant2>(
    ParamsT params,
    nv_bfloat16* tmp_v,
    float* tmp_s, cudaStream_t stream);
    

}