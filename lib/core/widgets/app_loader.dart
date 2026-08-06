import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import '../constants/asset_constants.dart';

class AppLoader extends StatelessWidget {
  final String? message;
  const AppLoader({super.key, this.message});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Use Lottie for high-quality loading state
          Lottie.asset(
            AssetConstants.loadingAnim,
            width: 150,
            height: 150,
            errorBuilder: (context, error, stackTrace) => const CircularProgressIndicator(),
          ),
          if (message != null) ...[
            const SizedBox(height: 16),
            Text(
              message!,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
          ],
        ],
      ),
    );
  }
}
