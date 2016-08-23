
import settings
import extractfeatures
import evaluate
import combinefeatures
import clusterfunctions


settings.init()
extractfeatures.use_dr_only()
combinefeatures.build_drwcg()

print("\nDone!")