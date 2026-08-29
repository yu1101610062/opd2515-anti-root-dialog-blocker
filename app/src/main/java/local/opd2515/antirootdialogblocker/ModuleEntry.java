// SPDX-License-Identifier: Apache-2.0
package local.opd2515.antirootdialogblocker;

import android.util.Log;

import java.lang.reflect.Method;
import java.util.concurrent.atomic.AtomicBoolean;

import io.github.libxposed.api.XposedInterface;
import io.github.libxposed.api.XposedModule;
import io.github.libxposed.api.XposedModuleInterface;

/**
 * Blocks the anti-root SYSTEM_DIALOG implementation in the validated
 * OPD2515 OplusExSystemService build.
 *
 * <p>The service is implemented by v6.b. Its Binder entry point is
 * v6.b$j.g0(int), while x() and y() build the forced-reboot and normal dialog
 * variants. All other SecureGuard processing remains intact.</p>
 */
public final class ModuleEntry extends XposedModule {
    private static final String TARGET_PACKAGE = "com.oplus.exsystemservice";
    private static final String TAG = "OPD2515-AntiRootDialogBlocker";
    private static final AtomicBoolean INSTALLED = new AtomicBoolean(false);

    public ModuleEntry() {}

    @Override
    public void onPackageLoaded(XposedModuleInterface.PackageLoadedParam param) {
        if (!TARGET_PACKAGE.equals(param.getPackageName())
                || !INSTALLED.compareAndSet(false, true)) {
            return;
        }

        try {
            ClassLoader loader = param.getDefaultClassLoader();
            int count = 0;
            count += blockMethods(loader, "v6.b", "x");
            count += blockMethods(loader, "v6.b", "y");
            count += blockMethods(loader, "v6.b$j", "g0");
            Log.i(TAG, "active; hooks=" + count);
        } catch (Throwable error) {
            INSTALLED.set(false);
            Log.e(TAG, "failed to install hooks", error);
        }
    }

    private int blockMethods(ClassLoader loader, String className, String methodName)
            throws ClassNotFoundException {
        Class<?> targetClass = Class.forName(className, false, loader);
        int count = 0;
        for (Method method : targetClass.getDeclaredMethods()) {
            if (!methodName.equals(method.getName())) {
                continue;
            }
            hook(method)
                    .setId(TAG + ":" + className + "." + methodName)
                    .setExceptionMode(XposedInterface.ExceptionMode.PROTECTIVE)
                    .intercept(new XposedInterface.Hooker() {
                        @Override
                        public Object intercept(XposedInterface.Chain chain) {
                            Log.i(TAG, "blocked " + className + "." + methodName);
                            return null;
                        }
                    });
            count++;
        }
        return count;
    }
}
