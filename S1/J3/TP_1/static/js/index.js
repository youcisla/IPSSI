document.addEventListener('DOMContentLoaded', () => {
	document.querySelectorAll('.edit-task').forEach(button => {
		button.addEventListener('click', async function() {
			const taskId = this.dataset.taskId;
			const span = document.getElementById('task-text-' + taskId);
			if(this.textContent === 'Edit') {
				const currentText = span.textContent;
				const input = document.createElement('input');
				input.type = 'text';
				input.className = 'form-control form-control-sm';
				input.value = currentText;
				span.parentNode.replaceChild(input, span);
				this.textContent = 'Save';
				const cancelBtn = document.createElement('button');
				cancelBtn.type = 'button';
				cancelBtn.className = 'btn btn-secondary btn-sm ms-2';
				cancelBtn.textContent = 'Cancel';
				this.parentNode.insertBefore(cancelBtn, this.nextSibling);
				cancelBtn.addEventListener('click', () => {
					input.parentNode.replaceChild(span, input);
					this.textContent = 'Edit';
					cancelBtn.remove();
				});
			} else {
				const input = this.parentNode.querySelector('input[type="text"]');
				const newText = input.value;
				const formData = new URLSearchParams();
				formData.append('id', taskId);
				formData.append('text', newText);
				const response = await fetch('/update_task', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/x-www-form-urlencoded'
					},
					body: formData.toString()
				});
				if(response.redirected) {
					window.location.reload();
				} else {
					span.textContent = newText;
					input.parentNode.replaceChild(span, input);
					this.textContent = 'Edit';
					const cancelBtn = this.parentNode.querySelector('button.btn-secondary');
					if(cancelBtn) cancelBtn.remove();
				}
			}
		});
	});
  
  // New listener for editing task priority
  document.querySelectorAll('.edit-priority').forEach(button => {
    button.addEventListener('click', async function() {
      const taskId = this.dataset.taskId;
      const badge = document.getElementById('task-priority-' + taskId);
      if(this.textContent.trim() === 'Edit Priority') {
        // Create select element with options
        const select = document.createElement('select');
        select.className = 'form-select form-select-sm';
        ['Low', 'Normal', 'High'].forEach(opt => {
          const option = document.createElement('option');
          option.value = opt;
          option.textContent = opt;
          if(opt === badge.textContent.trim()){
            option.selected = true;
          }
          select.appendChild(option);
        });
        badge.parentNode.replaceChild(select, badge);
        this.textContent = 'Save Priority';
        const cancelBtn = document.createElement('button');
        cancelBtn.type = 'button';
        cancelBtn.className = 'btn btn-secondary btn-sm ms-2';
        cancelBtn.textContent = 'Cancel';
        this.parentNode.insertBefore(cancelBtn, this.nextSibling);
        cancelBtn.addEventListener('click', () => {
          select.parentNode.replaceChild(badge, select);
          this.textContent = 'Edit Priority';
          cancelBtn.remove();
        });
      } else {
        const select = this.parentNode.querySelector('select.form-select');
        const newPriority = select.value;
        const formData = new URLSearchParams();
        formData.append('id', taskId);
        formData.append('priority', newPriority);
        const response = await fetch('/update_priority', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData.toString()
        });
        if(response.redirected) {
          window.location.reload();
        } else {
          badge.textContent = newPriority;
          if(newPriority === 'Low'){
            badge.className = 'badge bg-secondary';
          } else if(newPriority === 'High'){
            badge.className = 'badge bg-danger';
          } else {
            badge.className = 'badge bg-primary';
          }
          select.parentNode.replaceChild(badge, select);
          this.textContent = 'Edit Priority';
          const cancelBtn = this.parentNode.querySelector('button.btn-secondary');
          if(cancelBtn) cancelBtn.remove();
        }
      }
    });
  });
});
