from .models import Commission, Job, JobApplication
from django.db import transaction

class CommissionService:
    @staticmethod
    def create_commission(author, data, jobs_data):
        with transaction.atomic():
            commission = Commission.objects.create(
                maker=author,
                title=data['title'],
                description=data['description'],
                commission_type=data['commission_type'],
                people_required=data['people_required'],
                status=data.get('status', 'open')
            )

            for job in jobs_data:
                Job.objects.create(
                    commission=commission,
                    role=job['role'],
                    manpower_required=job['manpower_required'],
                    status=job.get('status', 'open')
                )
            return commission

    @staticmethod
    def apply_to_job(applicant, job):
        already_applied = JobApplication.objects.filter(
            applicant=applicant,
            job=job
        ).exists()
        if already_applied:
            raise ValueError("You have already applied to this job.")

        accepted_count = job.jobapplications.filter(status="accepted").count()
        if accepted_count >= job.manpower_required:
            raise ValueError("This job is already full.")

        return JobApplication.objects.create(
            applicant=applicant,
            job=job,
            status="pending"
        )

    @staticmethod
    def sync_commission_status(commission):
        jobs = commission.jobs.all()
        if jobs.exists() and all(job.status == "full" for job in jobs):
            commission.status = "full"
            commission.save()
    
    @staticmethod
    def get_commission_summary(commission):
        jobs = commission.jobs.all() 
        total_manpower = sum(job.manpower_required for job in jobs)
        accepted_counts = sum(job.jobapplications.filter(status="accepted").count() for job in jobs)
        open_manpower = total_manpower - accepted_counts
        jobs_with_status = []
        for job in jobs:
            job_accepted = job.jobapplications.filter(status="accepted").count()
            is_full = job_accepted >= job.manpower_required
            jobs_with_status.append({
                'job': job,
                'job_accepted':job_accepted,
                'is_full': is_full,
            })
        context = {
            "total_manpower": total_manpower,
            "open_manpower": open_manpower,
            "jobs_with_status": jobs_with_status
        }
        return context