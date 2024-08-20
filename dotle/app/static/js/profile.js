document.addEventListener('DOMContentLoaded', function() {
    const deleteForm = document.querySelector('.delform');
    
    deleteForm.addEventListener('keydown', function(event) {
      if (event.ctrlKey && (event.key === 'v' || event.key === 'V')) {
        event.preventDefault();
      }
    });
    
    deleteForm.addEventListener('paste', function(event) {
      event.preventDefault();
    });
  });