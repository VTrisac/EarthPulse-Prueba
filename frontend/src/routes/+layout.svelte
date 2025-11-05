<script>
  import '../app.css';
</script>

<div class="min-h-screen gradient-bg relative overflow-hidden">
  <!-- Floating decorative elements -->
  <div class="absolute top-20 left-10 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-float"></div>
  <div class="absolute bottom-20 right-10 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl animate-float" style="animation-delay: 2s;"></div>
  <div class="absolute top-1/2 left-1/2 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-float" style="animation-delay: 4s;"></div>

  <!-- Content -->
  <div class="relative z-10">
    <slot />
  </div>
</div>
